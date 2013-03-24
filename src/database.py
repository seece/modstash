import os
import logging
import psycopg2
import psycopg2.extras

if not 'DATABASE_URL' in os.environ:
	raise Exception("No database URL!")
else:
	print("Database URL found.")

schema = "ms"
dburl = os.environ['DATABASE_URL']

def connection():
	try:
		conn = psycopg2.connect(dburl)
	except Exception as e:
		print("Database error: " + str(e))
		raise

	return conn

def cursor(conn):
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	try:
		cur.execute("SET search_path TO " + schema + ";")
	except Exception as e:
		print("DB search path error: " + str(e))
		raise

	return cur

def test_connection():
	conn = connection()
	conn.close()
	return True
