import os
import string
import re

from unidecode import unidecode
import psycopg2
import database
from database import dbconnection
from lib.model.user import User
from lib.model.instrument import Instrument

class InvalidTrimmedNameException(Exception):
	"""Thrown if a name look up fails."""
	pass

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
	@dbconnection
	def get_authors(cls, songid, conn, cur):
		query = "SELECT * from author \
				WHERE songid=%s;"

		try:
			cur.execute(query,
					(songid,))
		except Exception as e:
			raise

		conn.commit()
		return cur.fetchall()
				
	@classmethod
	@dbconnection
	def get_by_trimmedname(cls, username, trimmedname, conn, cur):
		query = "SELECT songid FROM trimmedname \
				WHERE nicename = %s \
				AND songid in \
					(SELECT songid FROM author \
					WHERE username=%s);"

		try:
			cur.execute(query,
					(trimmedname, username))
		except Exception as e:
			print("Can't find song id: " + str(e))
			raise

		conn.commit()
		songid = cur.fetchone()['songid']

		if not songid:
			raise InvalidTrimmedNameException()

		return cls.get_by_id(songid)


	@classmethod
	@dbconnection
	def get_by_id(cls, songid, conn, cur):
		query = "SELECT * FROM song WHERE id = %s;"
		
		try:
			cur.execute(query,
					(songid,))
		except Exception as e:
			print("Can't find song: " + str(e))
			raise

		conn.commit()
		return cur.fetchone()

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
		return "" + filename

	@classmethod
	@dbconnection
	def finalize_title(cls, title, username, conn, cur):
		"""Appends letters to the given title until it's unique.
		
			The title is compared to the trimmed song names
			of the user. """

		songs = User.get_user_songs(username)
		finalname = title
		
		while True:
			hit = False
			for s in songs:
				if s['nicename'] == finalname:
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

		cls.add_instruments(song, songid)

		cls.save_to_disk(songbytes, songpath)

	@classmethod
	def add_instruments(cls, song, songid):
		"""Adds all (non-empty) instruments of the given song
		to the sample database."""

		for index, ins in enumerate(song.instruments):
			if not ins.sample:
				continue

			if ins.sample.length == 0:
				continue

			Instrument.add_instrument(songid, ins, index)
			








