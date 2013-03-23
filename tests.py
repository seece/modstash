import unittest
from test import test_password, test_database, test_templates

suites = []
pwtest 		= unittest.TestLoader().loadTestsFromTestCase(test_password.CredentialTests)
dbtest		= unittest.TestLoader().loadTestsFromTestCase(test_database.DatabaseTests)
temptest 	= unittest.TestLoader().loadTestsFromTestCase(test_templates.TemplateTests)
suites.append(pwtest)
suites.append(dbtest)
suites.append(temptest)

for s in suites:
	unittest.TextTestRunner(verbosity=1).run(s)


