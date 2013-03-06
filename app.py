import os
import cherrypy

port = 8080

if 'PORT' in os.environ:
	port = os.environ['PORT']

class HelloWorld:
	def index(self):
		return "MORO :D!"
	index.exposed = True

print("Using port: " + str(port))
cherrypy.config.update({'server.socket_host': '127.0.0.1',
						'server.socket_port': int(port),
                       })

cherrypy.quickstart(HelloWorld())
