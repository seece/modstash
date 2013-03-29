import os
import string
import psycopg2
import database
from database import dbconnection

class InvalidAuthorException(Exception):
	pass

class InvalidFilenameException(Exception):
	pass

# the last slash is mandatory
song_static_dir = './songs/'

'''Saves a song to the disk'''
def get_song_path(songbytes, song, songfile, username):

	song_dir = song_static_dir + username + os.sep
	if not os.path.exists(song_dir):
		os.makedirs(song_dir)
	
	filename = songfile.filename
	songpath = song_dir + filename

	# append underscores to the filename until it's unique
	rounds = 0
	while (os.path.exists(songpath)):
		filename = '_'*rounds + filename 
		songpath = os.path.join(song_dir, filename)
		rounds += 1

	return (songpath, filename)


class SongModel:
	@classmethod
	def save_to_disk(cls, songbytes, songpath):
		f = open(songpath, 'wb')
		f.write(songbytes)
		f.close()

	@classmethod
	def filename_to_url(cls, filename, username):
		return "/download/" + filename

	@classmethod
	@dbconnection
	def add_song(cls, song, songbytes, songfile, authors, conn, cur):
		if len(authors) == 0:
			raise InvalidAuthorException()

		if not songfile.filename or songfile.filename == "":
			raise InvalidFilenameException()

		songpath, real_filename = get_song_path(songbytes, song, songfile, authors[0])

		title = songfile.filename

		if song.name and song.name != "":
			title = song.name	

		# the first name in the author list is treated as the owner
		original_url = cls.filename_to_url(real_filename, authors[0])

		songquery = "INSERT INTO SONG (title, filename, original_url) \
				VALUES (%s, %s, %s) \
				RETURNING id;"
		authorquery = "INSERT INTO AUTHOR (songid, username, position, shown_name) \
				VALUES (%s, %s, %s, %s);"
		
		try:
			cur.execute(songquery,
					(title, songfile.filename, original_url))
		except Exception as e:
			print("Can't insert song: " + str(e))
			raise

		try:
			songid = cur.fetchone()['id']
			index = 0

			# we assume all authors are in the database
			# TODO check all author names first from the DB

			for name in authors:
				cur.execute(authorquery, (songid, name, index, name))
				index += 1
		except Exception as e:
			print("Can't insert author: " + str(e))
			raise

		conn.commit()

		cls.save_to_disk(songbytes, songpath)




