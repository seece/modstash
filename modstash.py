
import os
import cherrypy
from model import user
from mako.template import Template

index_template = Template(filename='templates/index.mako', output_encoding='utf-8')
#index_template = Template(filename='./templates/index.mako')

UserModel = user.UserModel

public_config = {'title': 'modstash'}


class lists:
	@cherrypy.expose
	def index(self, who):
		return "lists here " + str(who)


class Modstash:
	@cherrypy.expose
	def index(self):
		return index_template.render(config=public_config)

	@cherrypy.expose
	def users(self, who=None):

		if who==None:
			return "No who!"

		person = UserModel.get_user(who)

		return "yeah " + str(who) + " = " + str(person)

	@cherrypy.expose
	def adduser(self, name):
		details = {}
		details["username"] = name
		details["password"] = "PASSWORD"
		details["email"] = "e@mail.com" 
		print("trying to add ", name)
		return "jea: " + str(UserModel.add_user(details))
	


