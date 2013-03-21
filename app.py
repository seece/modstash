import os
import atexit
import cherrypy
import psycopg2

port = 8080
address = '0.0.0.0'
PATH = os.path.abspath(os.path.dirname(__file__))

if 'PORT' in os.environ:
	port = os.environ['PORT']
	print("PORT: " + str(port))

if 'ADDR' in os.environ:
	address = os.environ['ADDR']

if not 'DATABASE_URL' in os.environ:
	raise Exception("No database URL!")
else:
		print("Database URL found.")

dburl = os.environ['DATABASE_URL']

try:
	conn = psycopg2.connect(dburl)
except Exception as e:
	print("Database error: " + str(e))
	raise




def cleanup():
	conn.close()

atexit.register(cleanup)

class Modstash:
	@cherrypy.expose
	def index(self):
		return "modstash"

	@cherrypy.expose
	def add(self):
		cur = conn.cursor()
		result = "nothing"
		try:
			cur.execute("INSERT INTO ms.song (title, original_url, render_url) values (%s, %s, %s)", ("the title", "http://jea.mod", "http://song.mp3"))
			conn.commit()
		except Exception as e:
			print("Can't insert: " + str(e))

		try:
			cur.execute("SELECT * FROM ms.song;")	
			result = cur.fetchmany(100);
		except Exception as e:
			print("Can't list songs: " + str(e))


		cur.close()
		return "added! " + str(result)

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

start()
