import unittest
from lib.model.song import Song
from lib.model.song import get_static_song_path
from lib.model.song import InvalidAuthorException, InvalidFilenameException

class SongTests(unittest.TestCase):
	def setUp(self):
		pass

	def test_title_trim(self):
		self.assertEqual(Song.trim_title("a cat in  the hat"), "a-cat-in-the-hat")
		self.assertEqual(Song.trim_title("  hatter"), "hatter")
		self.assertEqual(Song.trim_title("maDDox   "), "maddox")
		self.assertEqual(Song.trim_title(" $spec1A£ sigNö ÄÄä  "), "spec1aps-signo-aaa")
		self.assertEqual(Song.trim_title("[[jeA]]/ %20   "), "jea-20")
		
	def test_static_file_path(self):
		self.assertEqual(get_static_song_path("user/song.mod"), "./songs/user/song.mod")
		