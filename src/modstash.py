import sys
import os
import cherrypy

from lib.modtag.modtag import load_module
from lib.model.user import User, UserDetailException, UserAlreadyExistsException
from lib.model.song import Song
from lib.model.sample import Sample
from view import *
from controller import Controller
from login import Login
from mako.template import Template
from mako.lookup import TemplateLookup
from lib.flash import flash
from lib.tool.restrict import restrict
	
cherrypy.tools.restrict = restrict

class Songpage(Controller):
	def __init__(self):
		pass

	def delete(username, songname):
		if not cherrypy.session.get('username'):
			raise cherrypy.HTTPError(401)

		if cherrypy.request.method != 'POST':
			raise cherrypy.HTTPError(404) 
			
		songid = Song.get_user_song(username, songname)
		Song.delete_song(songid)
		flash("Deleted '%s'" % (songname), 'success')
		raise cherrypy.HTTPRedirect("/users/" + username)

	@cherrypy.expose
	def index(self, username, songname, **args):
		try:
			song = Song.get_by_trimmedname(username, songname)
		except Exception as e:
			print(str(e))
			return self.render(error_view, 
					error_message="Song not found :(")
		
		if 'delete' in args:
			return Songpage.delete(username, songname)

		instruments = Song.get_instruments(song['id'])
		authors = Song.get_authors(song['id'])
		owner = authors[0]['username'] # the song owner has the song under his url

		# count the amount of references each instrument has
		# TODO use SQL to make this faster
		for ins in instruments:
			songs = Sample.get_sample_songs(ins['sampleid'])
			ins['songcount'] = len(songs)

		return self.render(song_view, song=song, authors=authors,
				owner=owner, nicename=songname, instruments=instruments)

class Modstash(Controller):
	"""The main controller object."""

	def __init__(self):
		login = Login()
		songpage = Songpage()
		self.login = login.login
		self.logout = login.logout
		#self.songpage = songpage.view
		self.songpage = Songpage.index
		#self.delete = songpage.delete

	@cherrypy.expose
	def index(self):
		top = Song.get_newest(40)
		return self.render(index_view, songs = top)

	@cherrypy.expose
	def songs(self, username, songname, **args):
		return self.songpage(self, username, songname, **args)

	@cherrypy.expose
	def users(self, who=None, **args):
		if not who:
			# TODO add user listing here?
			flash('Invalid user.', 'error')
			return self.render(error_view)

		person = User.get_user(who)

		if person == None:
			msg = "User '%s' not found!" % (str(who))
			return self.render(error_view, error_message=msg)

		sanitized = User.sanitize_user(person)
		songs = User.get_user_songs(person["username"])
		return self.render(user_view, user=sanitized, songs=songs)

	#@cherrypy.expose
	def adduser(self, name):
		details = {}
		details["username"] = name
		details["password"] = "PASSWORD"
		details["email"] = "e@mail.com" 
		print("trying to add ", name)
		return "jea: " + str(User.add_user(details))

	@cherrypy.expose
	def sample(self, sampleid):
		songs = Sample.get_sample_songs(sampleid)
		name = Sample.get_name(sampleid)
		return self.render(sample_view, songs=songs, sampleid=sampleid, samplename=name)

	@cherrypy.expose
	@cherrypy.tools.restrict()
	def uploadform(self):
		return self.render(upload_view)

	@cherrypy.expose
	@cherrypy.tools.restrict(method='POST')
	def upload(self, songfile):
		username=cherrypy.session.get('username')

		if not songfile:
			flash('Invalid file.', 'error')
			return self.render(index_view)
		
		songbytes = songfile.file.read()

		out = "<pre>%s %s %s</pre><br><pre>%s</pre>"

		try:
			song = load_module(songbytes)
		except Exception as e:
			flash("%s is not a valid module, only ProTracker modules are supported." % songfile.filename
					, 'error')
			return self.render(upload_view)

		Song.add_song(song, songbytes, songfile, [username,])

		flash("Song '%s' (%s) uploaded successfully." % (song.name, songfile.filename), 'success')
		raise cherrypy.HTTPRedirect("/users/%s" % (username, ))
		#return out % (len(songbytes), songfile.filename, songfile.content_type, song.name)

	@cherrypy.expose
	def register(self, username=None, password=None, password2=None, email=None):
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


		

