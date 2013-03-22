import os
import atexit
import cherrypy
import psycopg2
import database
from model import user
from modstash import *

port = 8080
address = '0.0.0.0'
PATH = os.path.abspath(os.path.dirname(__file__))

if 'PORT' in os.environ:
	port = os.environ['PORT']
	print("PORT: " + str(port))

if 'ADDR' in os.environ:
	address = os.environ['ADDR']

def start():
	globaldict = {
		'server.socket_host': address,
		'server.socket_port': int(port),
		'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
	}

	confdict =  {
	}

	cherrypy.config.update(globaldict)

	app = cherrypy.tree.mount(Modstash(), '/', "modstash.conf")
	app.merge(confdict)

	if hasattr(cherrypy.engine, "signal_handler"):
		cherrypy.engine.signal_handler.subscribe()
	if hasattr(cherrypy.engine, "console_control_handler"):
		cherrypy.engine.console_control_handler.subscribe()
	cherrypy.engine.start()
	cherrypy.engine.block()


def cleanup():
	pass

atexit.register(cleanup)
database.test_connection()
start()
