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

class User:
	@classmethod
	@dbconnection
	def get_user(cls, username, conn, cur):
		querystr = "SELECT * FROM Member WHERE username=%s"
		cur.execute(querystr, [username])
		victim = cur.fetchone()

		return victim

	@classmethod
	def sanitize_user(cls, user):
		"""Removes all private information from a user dictionary"""
		newuser = {
				'username'	: user['username'],
				'screen_name' : user['screen_name'],
				'last_logged' : user['last_logged'],
				'joined' : user['joined'],
				'member_type': user['member_type']
				}
		
		return newuser

	@classmethod
	def validate_credentials(cls, username, password):
		user = cls.get_user(username)

		if user==None:
			return False

		newhash = cls.hash_password(password, user["hash_salt"])

		print("OLD: ", user["password_hash"])
		print("NEW: ", newhash)

		if newhash != user["password_hash"]:
			return False

		return True


	@classmethod
	def validate_email(cls, address):
		if "@" in address:
			return True

		raise UserDetailException("Invalid email address.")

	@classmethod
	def validate_password(cls, password):
		if len(password) > 512:
			raise UserDetailException("Password too long (max 512 characters).")
		if len(password) == 0:
			raise UserDetailException("Blank password is not allowed.")
		return True

	"""Generates a randomized alphanumeric string of given length"""
	@classmethod
	def generate_salt(cls, length):
		salt = ''
		characters = string.ascii_letters + string.digits
		for x in range(length):
			salt = salt + random.choice(characters)
		return salt

	@classmethod
	def hash_password(cls, password, salt):
		if salt==None:
			salt=""

		wholestring = password + salt
		h = hashlib.new('sha256')
		h.update(wholestring.encode('utf-8'))
		return h.hexdigest()


	@classmethod
	def generate_hash(cls, password):
		"""Creates a password hash and a salt. Returned as a tuple."""
		salt = cls.generate_salt(96)
		wholestring = password + salt
		h = hashlib.new('sha256')
		h.update(wholestring.encode('utf-8'))

		return (h.hexdigest(), salt)

	
	@classmethod
	def validate_username(cls, username):
		"""Checks if a given username is free and valid"""
		if not username:
			raise UserDetailException("Blank username is not allowed.")

		if len(username) < 3 or len(username) > 32:
			raise UserDetailException("Invalid username. (Must be between 3-32 characters)")

		valid = re.match(r'^[\w_-]+$', username) is not None
		if not valid:
			raise UserDetailException("Username may contain only alphanumeric characters plus _ and -")

		if cls.get_user(username) != None:
			raise UserAlreadyExistsException()

		return True

	@classmethod
	@dbconnection
	def get_user_songs(cls, username, conn, cur):
		"""Loads all user song names from the database.
		Collaborations are loaded too. Does not load the actual
		song data, only ids and trimmed names."""

		query = 'SELECT songid, nicename FROM trimmedname \
				WHERE songid IN \
				(SELECT id FROM song WHERE \
					song.id IN \
					(SELECT songid FROM author WHERE username=%s));'

		cur.execute(query, (username,))
		conn.commit()
		result = cur.fetchall()
		return result

	@classmethod
	@dbconnection
	def log_visit(cls, username, conn, cur):
		"""Updates user's last_logged field"""
		query = 'UPDATE Member SET last_logged = CURRENT_TIMESTAMP \
				WHERE username = %s;'
		try:
			cur.execute(query, (username,))
		except Exception as e:
			print("Cannot update login information: %s" % (str(e)))

		conn.commit()

	@classmethod
	def add_user(cls, **args):
		required = ["username", "password", "email"]

		for r in required:
			if not r in args:
				raise UserDetailException("A required field is missing: %s" % r)

		cls.validate_username(args["username"])
		cls.validate_email(args["email"])
		cls.validate_password(args["password"])

		conn = database.connection()
		cur = database.cursor(conn)
		
		pwhash = cls.generate_hash(args["password"])
		screen_name = args["username"]

		query = "INSERT INTO Member \
				(username, screen_name, password_hash, hash_salt, email) \
				VALUES (%s, %s, %s, %s, %s)"

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
