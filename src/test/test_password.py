import unittest
import hashlib
from model.user import UserModel

class CredentialTests(unittest.TestCase):
	
	def setUp(self):
		pass

	def test_salt(self):
		for x in range(50, 100):
			salt = UserModel.generate_salt(x)
			self.assertEqual(x, len(salt))

	'''Check that the salt is concatenated to the pw'''
	def test_password_hash(self):
		password = 'supersecret' 
		h = hashlib.new('sha256')
		h.update(password.encode('utf-8'))

		properdigest = UserModel.generate_hash(password)
		self.assertNotEqual(h.hexdigest(), properdigest)

	def test_validate_username(self):
		self.assertFalse(UserModel.validate_username(""))
		self.assertFalse(UserModel.validate_username("q"))

	def test_validate_email(self):
		self.assertFalse(UserModel.validate_email(""))
		self.assertFalse(UserModel.validate_email("lol"))
		self.assertTrue(UserModel.validate_email("hello@example.com"))


