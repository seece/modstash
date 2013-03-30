import os
import string
import re
from unidecode import unidecode
import psycopg2
import database
from database import dbconnection

class InvalidAuthorException(Exception):
	pass

class InvalidFilenameException(Exception):
	pass

# the last slash is mandatory
song_static_dir = './songs/'

def get_song_path(songbytes, song, songfile, username):
	"""Saves a song to the disk"""

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

class Song:
	@classmethod
	def save_to_disk(cls, songbytes, songpath):
		f = open(songpath, 'wb')
		f.write(songbytes)
		f.close()

	@classmethod
	def trim_title(cls, title):
		"""Trims the given song title to be used in an URL"""
		trimmed = title.strip()
		trimmed = re.sub(r'\s+', '_', trimmed) # reduce whitespace to a single underscore
		trimmed = re.sub(r'_+', '_', trimmed)
		trimmed = re.sub(r'\W', '', trimmed)
		trimmed = unidecode(trimmed)
		trimmed = trimmed.lower()
		return trimmed

	@classmethod
	def filename_to_url(cls, filename, username):
		return "/download/" + filename

	@classmethod
	@dbconnection
	def finalize_title(cls, title, username, conn, cur):
		"""Appends letters to the given title until it's unique.
		
			The title is compared to the trimmed song names
			of the user. """
		query = 'SELECT songid, nicename FROM trimmedname \
				WHERE songid IN \
				(SELECT id FROM song WHERE \
					song.id IN \
					(SELECT id FROM author WHERE username=%s));'

		cur.execute(query, (username,))
		conn.commit()
		result = cur.fetchall()

		finalname = title
		
		while True:
			hit = False
			for r in result:
				if r['nicename'] == finalname:
					hit = True

			if not hit:
				break

			finalname += '_'

		return finalname

	@classmethod
	@dbconnection
	def add_song(cls, song, songbytes, songfile, authors, conn, cur):
		"""Adds a new song to the DB and saves the file to disk.
			
			Positional arguments:
			song		a tracker song object loaded with load_module
			songbytes	the binary representation of the song
			songfile	the file object passed in by cherrypy
			authors		the song authors as a list, the first one
						is considered the owner

		"""
		if len(authors) == 0:
			raise InvalidAuthorException()

		if not songfile.filename or songfile.filename == "":
			raise InvalidFilenameException()

		songid = None
		username = authors[0]
		songpath, real_filename = get_song_path(songbytes, song, songfile, username)

		title = songfile.filename

		if song.name and song.name != "":
			title = song.name	

		# the first name in the author list is treated as the owner
		original_url = cls.filename_to_url(real_filename, username)

		songquery = "INSERT INTO song (title, filename, original_url) \
				VALUES (%s, %s, %s) \
				RETURNING id;"
		authorquery = "INSERT INTO author (songid, username, position, shown_name) \
				VALUES (%s, %s, %s, %s);"
		namequery = "INSERT INTO trimmedname (songid, nicename) \
				VALUES (%s, %s);"
		
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

		nicename = cls.trim_title(title) or songfile.filename
		nicename = cls.finalize_title(nicename, username)

		try:
			cur.execute(namequery, (songid, nicename))
		except Exception as e:
			print("Can't insert trimmed name: " + str(e))
			raise

		conn.commit()

		cls.save_to_disk(songbytes, songpath)




