import unittest
import hashlib
from lib.model.user import User

class CredentialTests(unittest.TestCase):
	
	def setUp(self):
		pass

	def test_salt(self):
		for x in range(50, 100):
			salt = User.generate_salt(x)
			self.assertEqual(x, len(salt))

	'''Check that the salt is concatenated to the pw'''
	def test_password_hash(self):
		password = 'supersecret' 
		h = hashlib.new('sha256')
		h.update(password.encode('utf-8'))

		properdigest = User.generate_hash(password)
		self.assertNotEqual(h.hexdigest(), properdigest)

	def test_validate_username(self):
		self.assertFalse(User.validate_username(""))
		self.assertFalse(User.validate_username("q"))

	def test_validate_email(self):
		self.assertFalse(User.validate_email(""))
		self.assertFalse(User.validate_email("lol"))
		self.assertTrue(User.validate_email("hello@example.com"))


