import unittest
from test import test_password, test_database, test_templates, test_song

pwtest 		= unittest.TestLoader().loadTestsFromTestCase(test_password.CredentialTests)
dbtest		= unittest.TestLoader().loadTestsFromTestCase(test_database.DatabaseTests)
temptest 	= unittest.TestLoader().loadTestsFromTestCase(test_templates.TemplateTests)
songtest 	= unittest.TestLoader().loadTestsFromTestCase(test_song.SongTests)
suites = [pwtest, dbtest, temptest, songtest]

for s in suites:
	unittest.TextTestRunner(verbosity=1).run(s)


