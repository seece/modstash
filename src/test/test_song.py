import unittest
from model.song import Song
from model.song import InvalidAuthorException, InvalidFilenameException

class SongTests(unittest.TestCase):
	def setUp(self):
		pass

	def test_title_trim(self):
		self.assertEqual(Song.trim_title("a cat in  the hat"), "a_cat_in_the_hat")
		self.assertEqual(Song.trim_title("  hatter"), "hatter")
		self.assertEqual(Song.trim_title("maDDox   "), "maddox")
		self.assertEqual(Song.trim_title(" $spec1A£ sigNö ÄÄä  "), "spec1a_signo_aaa")
		self.assertEqual(Song.trim_title("[[jeA]]/ %20   "), "jea_20")
		
		