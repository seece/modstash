import unittest
from model.song import SongModel
from model.song import InvalidAuthorException, InvalidFilenameException

class SongTests(unittest.TestCase):
	def setUp(self):
		pass

	def test_title_trim(self):
		self.assertEqual(SongModel.trim_title("a cat in  the hat"), "a_cat_in_the_hat")
		self.assertEqual(SongModel.trim_title("  hatter"), "hatter")
		self.assertEqual(SongModel.trim_title("maDDox   "), "maddox")
		self.assertEqual(SongModel.trim_title(" $spec1A£ sigNö ÄÄä  "), "spec1a_signo_aaa")
		self.assertEqual(SongModel.trim_title("[[jeA]]/ %20   "), "jea_20")
		
		