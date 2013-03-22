
import cherrypy

class Modstash:
	@cherrypy.expose
	def index(self):
		return "modstash"

	@cherrypy.expose
	def add(self):
		return "not added"
