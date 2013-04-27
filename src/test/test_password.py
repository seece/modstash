import unittest
import hashlib
import lib.model.user as User

class CredentialTests(unittest.TestCase):
	
	def setUp(self):
		pass

	def test_salt(self):
		for x in range(50, 100):
			salt = User.generate_salt(x)
			self.assertEqual(x, len(salt))

	def test_password_hash(self):
		"""Check that the salt is concatenated to the pw"""
		password = 'supersecret' 
		h = hashlib.new('sha256')
		h.update(password.encode('utf-8'))

		properdigest = User.generate_hash(password)
		self.assertNotEqual(h.hexdigest(), properdigest)

	def test_validate_username(self):
		self.assertRaises(User.UserDetailException, User.validate_username, "")
		self.assertRaises(User.UserDetailException, User.validate_username, "q")
		self.assertTrue(User.validate_username("kuapo"))

	def test_validate_email(self):
		self.assertRaises(User.UserDetailException, User.validate_email, "")
		self.assertRaises(User.UserDetailException, User.validate_email, "-_sda q")
		self.assertTrue(User.validate_email("hello@example.com"))


