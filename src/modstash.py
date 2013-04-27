import sys
import os
import cherrypy

from lib.modtag.modtag import load_module
import lib.model.user as User
from lib.model.user import UserDetailException, UserAlreadyExistsException
import lib.model.song as Song
import lib.model.influence as Influence 
import lib.model.sample as Sample
from view import *
from lib.flash import flash
from lib.tool.restrict import restrict

from controller import Controller
from login import Login
from songpage import Songpage 
	
cherrypy.tools.restrict = restrict

def handle_error():
	cherrypy.response.status = 500
	cherrypy.response.body = "<p>Internal error occured! We are terribly sorry :(</p>"
	return ""

class Modstash(Controller):
	"""The main controller object."""

	def __init__(self):
		login = Login()
		songpage = Songpage()
		self.login = login.login
		self.logout = login.logout
		self.songpage = Songpage.index

	@cherrypy.expose
	def index(self):
		"""The index page handler."""
		top = Song.get_newest(40)
		return self.render(index_view, songs = top)

	@cherrypy.expose
	def loginform(self):
		"""The login page handler."""
		return self.render(login_view)

	@cherrypy.expose
	def songs(self, username, songname, **args):
		"""The user song listing page handler."""

		return self.songpage(self, username, songname, **args)

	@cherrypy.expose
	def users(self, who=None, **args):
		"""User detail page handler."""
		if not who:
			# TODO add user listing here?
			flash('Invalid user.', 'error')
			return self.render(error_view)

		person = User.get_user(who)

		if person == None:
			msg = "User '%s' not found!" % (str(who))
			return self.render(error_view, error_message=msg)

		sanitized = User.sanitize_user(person)
		songs = User.get_user_songs_detailed(person["username"])
		return self.render(user_view, user=sanitized, songs=songs)

	@cherrypy.expose
	def sample(self, sampleid):
		"""Sample detail page handler."""

		songs = Sample.get_sample_songs(sampleid)
		name = Sample.get_name(sampleid)
		return self.render(sample_view, songs=songs, sampleid=sampleid, samplename=name)

	@cherrypy.expose
	@cherrypy.tools.restrict()
	def uploadform(self):
		"""Song upload form handler."""
		return self.render(upload_view)

	@cherrypy.expose
	@cherrypy.tools.restrict(method='POST')
	def upload(self, songfile, influence, influence_type):
		"""Song upload POST endpoint."""

		username=cherrypy.session.get('username')

		if not songfile:
			flash('Invalid file.', 'error')
			raise cherrypy.HTTPRedirect("/uploadform")

		if not songfile.file:
			flash('Invalid file.', 'error')
			raise cherrypy.HTTPRedirect("/uploadform")
		
		songbytes = songfile.file.read()

		try:
			song = load_module(songbytes)
		except Exception as e:
			flash("%s is not a valid module, only ProTracker modules are supported." % songfile.filename
					, 'error')
			return self.render(upload_view)

		if influence and not influence_type:
			flash("Invalid influence type!")
			raise cherrypy.HTTPRedirect("/uploadform")

		songid = Song.add_song(song, songbytes, songfile, [username,])

		flash("Song uploaded successfully.", 'success')

		if influence and influence != 'empty':
			influence_id = None

			try:
				influence_id = Influence.get_song_id_from_url(influence)
			except Exception as e:
				flash("Cannot parse influence url!", 'error')
				flash("Error: " + str(e), 'error')

			try:
				Influence.add_internal_influence(influence_id, songid, influence_type)
			except Exception as e:
				flash("Song influences were not added.", 'notice')
				flash("Error: " + str(e), 'error')

		raise cherrypy.HTTPRedirect("/users/%s" % (username, ))

	@cherrypy.expose
	def register(self, username=None, password=None, password2=None, email=None):
		"""Registration form page handler."""

		if cherrypy.request.method == 'GET':
			return self.render(register_view)

		if cherrypy.request.method != 'POST':
			raise cherrypy.HTTPError(404) 

		try:
			if password != password2:
				raise UserDetailException("Passwords do not match.")

			User.add_user(username=username, password=password, email=email)
		except UserDetailException as e:
			flash(str(e), 'error')
			return self.render(register_view)
		except UserAlreadyExistsException as e:
			flash("User already exists with that name.", 'error')
			return self.render(register_view)
		else:
			flash("Account created successfully! You can now log in.", 'success')
			raise cherrypy.HTTPRedirect('/')


		

