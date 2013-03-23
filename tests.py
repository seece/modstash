import unittest
from test import test_password, test_database

suites = []
pwtest = unittest.TestLoader().loadTestsFromTestCase(test_password.CredentialTests)
dbtest= unittest.TestLoader().loadTestsFromTestCase(test_database.DatabaseTests)
suites.append(pwtest)
suites.append(dbtest)

for s in suites:
	unittest.TextTestRunner(verbosity=2).run(s)


