import re
import string
import hashlib
import random
import psycopg2
import database
from database import dbconnection

class UserAlreadyExistsException(Exception):
	pass

class UserDetailException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

@dbconnection
def get_user(username, conn, cur):
	"""Fetch user details with the matchin username."""
	querystr = "SELECT * FROM Member WHERE username=%s"
	cur.execute(querystr, [username])
	victim = cur.fetchone()

	return victim

def sanitize_user(user):
	"""Removes all private information from a user dictionary."""
	newuser = {
			'username'	: user['username'],
			'screen_name' : user['screen_name'],
			'last_logged' : user['last_logged'],
			'joined' : user['joined'],
			'member_type': user['member_type']
			}
	
	return newuser

def validate_credentials(username, password):
	"""
	Checks if a matching username & password pair exists
	in the database.
	"""

	user = get_user(username)

	if user==None:
		return False

	newhash = hash_password(password, user["hash_salt"])

	if newhash != user["password_hash"]:
		return False

	return True


def validate_email(address):
	"""
	Validate an email address.
	Throws UserDetailException on failure.
	"""

	if "@" in address:
		return True

	raise UserDetailException("Invalid email address.")

def validate_password(password):
	"""
	Validate a password.
	Throws UserDetailException on failure.
	"""

	if len(password) > 512:
		raise UserDetailException("Password too long (max 512 characters).")
	if len(password) == 0:
		raise UserDetailException("Blank password is not allowed.")
	return True


def generate_salt(length):
	"""Generates a randomized alphanumeric string of given length"""

	salt = ''
	characters = string.ascii_letters + string.digits
	for x in range(length):
		salt = salt + random.choice(characters)
	return salt

def hash_password(password, salt):
	"""Hashes a password together with the given salt."""

	if salt==None:
		salt=""

	wholestring = password + salt
	h = hashlib.new('sha256')
	h.update(wholestring.encode('utf-8'))
	return h.hexdigest()


def generate_hash(password):
	"""Creates a password hash and a salt. Returned as a tuple."""
	salt = generate_salt(96)
	wholestring = password + salt
	h = hashlib.new('sha256')
	h.update(wholestring.encode('utf-8'))

	return (h.hexdigest(), salt)


def validate_username(username):
	"""Checks if a given username is free and valid"""
	if not username:
		raise UserDetailException("Blank username is not allowed.")

	if len(username) < 3 or len(username) > 32:
		raise UserDetailException("Invalid username. (Must be between 3-32 characters)")

	valid = re.match(r'^[\w_-]+$', username) is not None
	if not valid:
		raise UserDetailException("Username may contain only alphanumeric characters plus _ and -")

	if get_user(username) != None:
		raise UserAlreadyExistsException()

	return True

@dbconnection
def get_user_songs(username, conn, cur):
	"""
	Loads all user song names & id's from the database.
	Collaborations are loaded too. Does not load the actual
	song data, only id's and trimmed names.
	"""

	query = """
			SELECT songid, nicename FROM trimmedname 
			WHERE songid IN 
			(SELECT s.id FROM song s 
				INNER JOIN author a ON a.songid=s.id 
				AND a.username = %s);
			"""

	cur.execute(query, (username,))
	conn.commit()
	result = cur.fetchall()
	return result

@dbconnection
def get_user_songs_detailed(username, conn, cur):
	"""
	Gets all details from all songs where the user
	is marked being an author.
	"""

	query = """
			SELECT * FROM trimmedname, song 
			WHERE songid IN 
			(SELECT s.id FROM song s 
				INNER JOIN author a ON a.songid=s.id 
				AND a.username = %s) 
			AND song.id = trimmedname.songid 
			ORDER BY upload_date DESC;
			"""
	cur.execute(query, (username,))
	result = cur.fetchall()

	return result

@dbconnection
def log_visit(username, conn, cur):
	"""Updates user's last_logged field."""

	query = """
			UPDATE Member SET last_logged = CURRENT_TIMESTAMP
			WHERE username = %s;
			"""
	try:
		cur.execute(query, (username,))
	except Exception as e:
		print("Cannot update login information: %s" % (str(e)))

	conn.commit()

def add_user(**args):
	"""
	Adds a user to the database.
	Throws UserDetailException on failure.
	"""

	required = ["username", "password", "email"]

	for r in required:
		if not r in args:
			raise UserDetailException("A required field is missing: %s" % r)

	validate_username(args["username"])
	validate_email(args["email"])
	validate_password(args["password"])

	conn = database.connection()
	cur = database.cursor(conn)
	
	pwhash = generate_hash(args["password"])
	screen_name = args["username"]

	query = """
			INSERT INTO Member 
			(username, screen_name, password_hash, hash_salt, email) 
			VALUES (%s, %s, %s, %s, %s)
			"""

	try:
		cur.execute(query, 
				(args["username"], screen_name, 
				pwhash[0], pwhash[1], args["email"]))
	except Exception as e:
		print("Can't insert user: " + str(e))
		raise

	conn.commit()

	cur.close()
	conn.close()
