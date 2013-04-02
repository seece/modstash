
import sys
import os
import cherrypy

from lib.modtag.modtag import load_module
from lib.model.user import User
from lib.model.song import Song
from view import *
from controller import Controller
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
			
		songid = Song.get_id_from_trimmedname(username, songname)
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
		
		if 'delete'  in args:
			return Songpage.delete(username, songname)
			

		authors = Song.get_authors(song['id'])
		owner = None # the song owner has the song under his url

		for a in authors:
			if a['position'] == 0:
				owner = a['username']
				break

		return self.render(song_view, song=song, authors=authors,
				owner=owner, nicename=songname)

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
		return self.render(index_view)

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
			flash("%s is not a valid module, only amiga modules are supported." % songfile.filename
					, 'error')
			return self.render(upload_view)

		Song.add_song(song, songbytes, songfile, [username,])

		return out % (len(songbytes), songfile.filename, songfile.content_type, song.name)

		
class Login(Controller):
	@cherrypy.expose
	def login(self, username=None, password=None):
		if cherrypy.request.method != "POST":
			raise cherrypy.HTTPError(404)

		if cherrypy.session.get('username'):
			flash("You have already logged in.")
			return self.render(index_view)

		valid = User.validate_credentials(username, password)

		if valid:
			User.log_visit(username)
			cherrypy.session['username'] = username
			cherrypy.session.save()
			flash("Logged in successfully!", 'success')

			# redirect user back to the page where login was entered
			raise cherrypy.HTTPRedirect(cherrypy.request.headers.get("Referer", "/") or "/")
		else:
			flash("Invalid credentials.", 'error')
			return self.render(index_view)
			
	@cherrypy.expose
	def logout(self):
		username=cherrypy.session.get('username')

		if not username:
			flash("You haven't logged in.", 'error')
			return self.render(error_view, error_message="Please login before logging out, because you cannot logout before you have logged in.")
					
		cherrypy.session.clear()
		flash("Logged out successfully!", 'success')
		forward_url = cherrypy.request.headers.get("Referer", "/")
		raise cherrypy.HTTPRedirect(forward_url or "/")


