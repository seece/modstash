import os
import cherrypy
#import sqlalchemy
#from sqlalchemy import create_engine
#from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

port = 8080

if 'PORT' in os.environ:
	port = os.environ['PORT']

if not 'DATABASE_URL' in os.environ:
	raise Exception("No database URL!")
else:
		print("Database URL found.")

#dburl = os.environ['DATABASE_URL']
#engine = create_engine(dburl, echo=True)


#metadata = MetaData()
#metadata.create_all(engine)

class HelloWorld:
	def index(self):
		return "MORO :D!"
	index.exposed = True

print("Using port " + str(port))
cherrypy.config.update({'server.socket_host': '0.0.0.0',
						'server.socket_port': int(port),
                       })

cherrypy.quickstart(HelloWorld())
