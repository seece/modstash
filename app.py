import os
import cherrypy

port = 8080

if PORT in os.environ:
	port = os.environ['PORT']

class HelloWorld:
	def index(self):
		return "MORO :D!"
	index.exposed = True

cherrypy.server.socket_port = port
cherrypy.quickstart(HelloWorld())
