import os
import cherrypy
import sqlalchemy
from sqlalchemy import create_engine

port = 8080

if 'PORT' in os.environ:
	port = os.environ['PORT']

if not 'DATABASE_URL' in os.environ:
	raise Exception("No database URL!")
else:
		print("Database URL found.")

class HelloWorld:
	def index(self):
		return "MORO :D!"
	index.exposed = True

print("Using port " + str(port))
cherrypy.config.update({'server.socket_host': '0.0.0.0',
						'server.socket_port': int(port),
                       })

cherrypy.quickstart(HelloWorld())
