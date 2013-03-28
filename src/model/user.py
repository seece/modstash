import string
import hashlib
import random
from functools import wraps
import psycopg2
import database

'''A decorator that provides a database connection and 
a related cursor to the function'''
def dbconnection(f):
	@wraps(f)
	def connection_wrapper(*args, **kwargs):
		conn = database.connection()
		cur = database.cursor(conn) 
		kwargs['conn'] = conn
		kwargs['cur'] = cur 

		result = f(*args, **kwargs)
		cur.close()
		conn.close()
		return result
	return connection_wrapper

class UserAlreadyExistsException(Exception):
	pass

class UserDetailException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

'''A user record'''
class User:
	def __init__(self):
		fields = {}

		fields["username"] = None
		fields["screen_name"] = None
		fields["password_hash"] = None
		fields["hash_salt"] = None
		fields["last_logged"] = None
		fields["joined"] = None
		fields["email"] = None
		fields["auth_token"] = None

		self.fields = fields

	'''Initializes the object from database query result'''
	def load_from_result(self, result):
		print(str(result))
		pass

	def print_info(self):
		print(self.username + ", " + self.screen_name + ", " + self.email)

	
class UserModel:
	@classmethod
	@dbconnection
	def get_user(cls, username, conn, cur):
		querystr = "SELECT * FROM Member WHERE username=%s"
		cur.execute(querystr, [username])
		victim = cur.fetchone()

		return victim

	'''Removes all private information from a user dictionary'''
	@classmethod
	def sanitize_user(cls, user):
		newuser = {
				'username'	: user['username'],
				'screen_name' : user['screen_name'],
				'last_logged' : user['last_logged'],
				'joined' : user['joined'],
				'member_type': user['member_type']
				}
		
		return newuser

	@classmethod
	def get_user_object(cls, username):
		result = cls.get_user(username)

		if result==None:
			return None

		obj = User()
		obj.load_from_result(result)
		return obj


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

		return False

	@classmethod
	def validate_password(cls, password):
		if len(password) < 2:
			return False
		return True

	'''Generates a randomized alphanumeric string of given length'''
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


	'''Creates a password hash and a salt. Returned as a tuple.'''
	@classmethod
	def generate_hash(cls, password):
		salt = cls.generate_salt(96)
		wholestring = password + salt
		h = hashlib.new('sha256')
		h.update(wholestring.encode('utf-8'))

		return (h.hexdigest(), salt)

	
	'''Checks if a given username is free and valid'''
	@classmethod
	def validate_username(cls, username):
		if len(username) < 3:
			return False

		if cls.get_user(username) != None:
			raise UserAlreadyExistsException()

		return True

	'''Updates user's last_logged field'''
	@classmethod
	@dbconnection
	def log_visit(cls, username, conn, cur):
		query = 'UPDATE Member SET last_logged = CURRENT_TIMESTAMP \
				WHERE username = %s;'
		try:
			cur.execute(query, (username,))
		except Exception as e:
			print("Cannot update login information: %s" % (str(e)))

		conn.commit()

	@classmethod
	def add_user(cls, details):
		required = ["username", "password", "email"]

		for r in required:
			if not r in details:
				raise UserDetailException(r)

		if not cls.validate_username(details["username"]):
			raise UserDetailException("Invalid username.")

		if not cls.validate_email(details["email"]):
			raise UserDetailException("Invalid email address.")

		if not cls.validate_password(details["password"]):
			raise UserDetailException("That's an awful password.")

		conn = database.connection()
		cur = database.cursor(conn)
		
		pwhash = cls.generate_hash(details["password"])
		screen_name = details["username"]

		query = "INSERT INTO Member \
				(username, screen_name, password_hash, hash_salt, email) \
				VALUES (%s, %s, %s, %s, %s)"

		try:
			cur.execute(query, 
					(details["username"], screen_name, 
					pwhash[0], pwhash[1], details["email"]))
		except Exception as e:
			print("Can't insert user: " + str(e))
			raise

		conn.commit()

		cur.close()
		conn.close()
