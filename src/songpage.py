import sys
import os
import cherrypy

from lib.modtag.modtag import load_module
import lib.model.user as User
from lib.model.user import UserDetailException, UserAlreadyExistsException
import lib.model.song as Song
import lib.model.influence as Influence
import lib.model.sample as Sample
from lib.flash import flash
from view import *
from controller import Controller

class Songpage(Controller):
	"""The songpage controller class."""
	def __init__(self):
		pass

	def delete(username, songname):
		"""Attempts to delete a song."""

		if not cherrypy.session.get('username'):
			raise cherrypy.HTTPError(401)

		if cherrypy.request.method != 'POST':
			raise cherrypy.HTTPError(404) 

		current_user = cherrypy.session.get('username')
		user = User.get_user(current_user)

		if user['member_type'] != 'admin':
			if current_user != username:
				raise cherrypy.HTTPError(401)
			
		songid = Song.get_user_song(username, songname)
		Song.delete_song(songid)
		flash("Deleted '%s'" % (songname), 'success')
		raise cherrypy.HTTPRedirect("/users/" + username)

	@cherrypy.expose
	def index(self, username, songname, **args):
		"""Lists song details, if possible."""

		try:
			song = Song.get_by_trimmedname(username, songname)
		except Exception as e:
			print(str(e))
			return self.render(error_view, 
					error_message="Song not found :(")
		
		if 'delete' in args:
			return Songpage.delete(username, songname)

		instruments = Song.get_instruments(song['id'], refcount=True)
		authors = Song.get_authors(song['id'])
		owner = authors[0]['username'] # the song owner has the song under his url
		influences = Influence.get_song_influences(song['id'])

		return self.render(song_view, song=song, authors=authors,
				owner=owner, nicename=songname, instruments=instruments,
				influences=influences)
