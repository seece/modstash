import unittest
import hashlib
from model.user import UserModel

class PasswordTests(unittest.TestCase):
	
	def setUp(self):
		pass

	def test_salt(self):
		length = 100
		salt = UserModel.generate_salt(length)
		self.assertEqual(length, len(salt))

	'''Check that the salt is concatenated to the pw'''
	def test_password_hash(self):
		password = 'supersecret' 
		h = hashlib.new('sha256')
		h.update(password.encode('utf-8'))

		properdigest = UserModel.hash_password(password)
		self.assertNotEqual(h.hexdigest(), properdigest)



