
import os
import cherrypy
from model import user
from view import *
from mako.template import Template
from mako.lookup import TemplateLookup
from flash import flash

UserModel = user.UserModel

'''The main controller class. '''
class Controller:
	def __init__(self):
		pass

	'''Renders a template with some parameters pulled from the active session'''
	def render(self, view, **params):
		username=cherrypy.session.get('username')
		logged_in = username!=None

		if not 'error_message' in params:
			params['error_message'] = ''

		params['flash'] = flash=cherrypy.session.get('flash')
		params['username'] = username
		params['logged_in'] = logged_in
		return view.render(**params)

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
			cherrypy.session['username'] = username
			cherrypy.session.save()
			flash("Logged in successfully!", 'success')
			return self.render(index_view)
		else:
			flash("Invalid credentials.", 'error')
			return self.render(index_view)
	


