
import sys
import os
import cherrypy

from modtag.modtag import load_module
from model.user import UserModel
from model.song import SongModel
from view import *
from controller import Controller
from mako.template import Template
from mako.lookup import TemplateLookup
from flash import flash
from restrict import restrict

cherrypy.tools.restrict = restrict

class Modstash(Controller):
	@cherrypy.expose
	def index(self):
		return self.render(index_view)

	@cherrypy.expose
	def users(self, who=None):
		if not who:
			# TODO add user listing here?
			flash('Invalid user.', 'error')
			return self.render(error_view)

		person = UserModel.get_user(who)

		if person == None:
			msg = "User '%s' not found!" % (str(who))
			return self.render(error_view, error_message=msg)

		sanitized = UserModel.sanitize_user(person)
		return self.render(user_view, user=sanitized)

	#@cherrypy.expose
	def adduser(self, name):
		details = {}
		details["username"] = name
		details["password"] = "PASSWORD"
		details["email"] = "e@mail.com" 
		print("trying to add ", name)
		return "jea: " + str(UserModel.add_user(details))

	@cherrypy.expose
	@cherrypy.tools.restrict()
	def uploadform(self):
		return self.render(upload_view)

	@cherrypy.expose
	@cherrypy.tools.restrict()
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

		SongModel.add_song(song, songbytes, songfile, [username,])

		return out % (len(songbytes), songfile.filename, songfile.content_type, song.name)

	@cherrypy.expose
	def logout(self):
		username=cherrypy.session.get('username')

		if not username:
			flash("You haven't logged in.", 'error')
			return self.render(error_view, error_message="Please login before logging out, because you cannot logout before you have logged in.")
					

		cherrypy.session.clear()
		flash("Logged out successfully!", 'success')
		return self.render(index_view)


	@cherrypy.expose
	def login(self, username=None, password=None):
		if cherrypy.request.method != "POST":
			raise cherrypy.HTTPError(404)

		if cherrypy.session.get('username'):
			flash("You have already logged in.")
			return self.render(index_view)

		valid = UserModel.validate_credentials(username, password)

		if valid:
			UserModel.log_visit(username)
			cherrypy.session['username'] = username
			cherrypy.session.save()
			flash("Logged in successfully!", 'success')
			return self.render(index_view)
		else:
			flash("Invalid credentials.", 'error')
			return self.render(index_view)
	


