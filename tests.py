import unittest
from test import test_password

suite = unittest.TestLoader().loadTestsFromTestCase(test_password.PasswordTests)
unittest.TextTestRunner(verbosity=2).run(suite)

