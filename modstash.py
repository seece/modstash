
import cherrypy
from model import user

UserModel = user.UserModel


class lists:
	@cherrypy.expose
	def index(self, who):
		return "lists here " + str(who)


class Modstash:
	@cherrypy.expose
	def index(self):
		return "modstash"

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
	


