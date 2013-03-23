import string
import hashlib
import random
import psycopg2
import database

class UserAlreadyExistsException(Exception):
	pass

class UserDetailException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

'''A user record'''
class User:
	def __init__(self):
		'''
		self.username = None
		self.screen_name = None
		self.password_hash = None
		self.hash_salt = None
		self.last_logged = None
		self.joined = None
		self.email = None
		self.auth_token = None
		'''
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

	def print_info(self):
		print(self.username + ", " + self.screen_name + ", " + self.email)

	
class UserModel:
	@classmethod
	def get_user(cls, username):
		conn = database.connection()
		cur = database.cursor(conn) 

		querystr = "SELECT * FROM Member WHERE username=%s"
		cur.execute(querystr, [username])
		victim = cur.fetchone()

		cur.close()
		conn.close()

		return victim

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


	'''Creates a password hash and a salt. Returned as a tuple.'''
	@classmethod
	def hash_password(cls, password):
		salt = cls.generate_salt(96)
		wholestring = password + salt
		h = hashlib.new('sha256')
		h.update(wholestring.encode('utf-8'))

		return (h.hexdigest(), salt)

	@classmethod
	def validate_username(cls, username):
		if cls.get_user(username) != None:
			raise UserAlreadyExistsException()

		if len(username) == 0:
			return False

		return True

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
		
		pwhash = cls.hash_password(details["password"])
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
