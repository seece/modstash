
import os
import cherrypy
from model import user
from view import View
from mako.template import Template
from mako.lookup import TemplateLookup

UserModel = user.UserModel
index_view = View('templates/index.html')

class lists:
	@cherrypy.expose
	def index(self, who):
		return "lists here " + str(who)


class Modstash:
	@cherrypy.expose
	def index(self):
		return index_view.render()

	@cherrypy.expose
	def users(self, who=None):

		if who==None:
			return "No who!"

		person = UserModel.get_user(who)

		if person == None:
			return "no hit"

		return "yeah " + str(who) + " = " + str(len(person)) + " fields!" 

	#@cherrypy.expose
	def adduser(self, name):
		details = {}
		details["username"] = name
		details["password"] = "PASSWORD"
		details["email"] = "e@mail.com" 
		print("trying to add ", name)
		return "jea: " + str(UserModel.add_user(details))

	@cherrypy.expose
	def login(self, username=None, password=None):
		if cherrypy.request.method != "POST":
			raise cherrypy.HTTPError(404)

		print("USERNAME: " + str(username))
		if password==None: 
			print("PASSWORD: NO")
		else:
			print("PASSWORD: YES")

		valid = UserModel.validate_credentials(username, password)

		print("VALID: " + str(valid))

		if valid:
			return "success"
		else:
			return "invalid username or password"
	


