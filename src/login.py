import sys
import os
import cherrypy

import lib.model.user as User
from view import *
from controller import Controller
from mako.template import Template
from mako.lookup import TemplateLookup
from lib.flash import flash
from lib.tool.restrict import restrict
	
cherrypy.tools.restrict = restrict

class Login(Controller):
	"""	The login controller. 
		Takes care of signing users in and out.

	"""
	
	@cherrypy.expose
	def login(self, username=None, password=None):
		"""The login POST endpoint."""
		if cherrypy.request.method != "POST":
			raise cherrypy.HTTPError(404)

		if cherrypy.session.get('username'):
			flash("You have already logged in.")
			raise cherrypy.HTTPRedirect(cherrypy.request.headers.get("Referer", "/") or "/")

		valid = User.validate_credentials(username, password)
		status = User.get_user(username)['member_type']

		if not valid:
			flash("Invalid credentials.", 'error')
			raise cherrypy.HTTPRedirect(cherrypy.request.headers.get("Referer", "/") or "/")

		if status == 'banned':
			flash("You can't login, you are banned!", 'error')
			raise cherrypy.HTTPRedirect('/')

		User.log_visit(username)
		cherrypy.session['username'] = username
		cherrypy.session.save()
		flash("Logged in successfully!", 'success')

		# redirect user back to the page where login was entered
		raise cherrypy.HTTPRedirect(cherrypy.request.headers.get("Referer", "/") or "/")

			
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


