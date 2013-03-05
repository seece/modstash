import cherrypy

class HelloWorld:
	def index(self):
		return "MORO :D!"
	index.exposed = True

cherrypy.quickstart(HelloWorld())
