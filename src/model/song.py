import os
import string
import psycopg2
import database
from database import dbconnection


# the last slash is mandatory
song_static_dir = './songs/'

'''Saves a song to the disk'''
def save_song(songbytes, song, songfile, username):
	title = songfile.filename

	if song.name and song.name != "":
		title = song.name	

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

	f = open(songpath, 'wb')
	f.write(songbytes)
	f.close()

	return filename


class SongModel:
	pass

