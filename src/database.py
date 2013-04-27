import os
import logging
from functools import wraps
import psycopg2
import psycopg2.extras

if not 'DATABASE_URL' in os.environ:
	raise Exception("No database URL!")
else:
	print("Database URL found.")

schema = "ms"
dburl = os.environ['DATABASE_URL']

def connection():
	"""Returns a database connection."""

	try:
		conn = psycopg2.connect(dburl)
	except Exception as e:
		print("Database error: " + str(e))
		raise

	return conn

def cursor(conn):
	"""Returns the database cursor with the correct schema already set."""
	
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	try:
		cur.execute("SET search_path TO " + schema + ";")
	except Exception as e:
		print("DB search path error: " + str(e))
		raise

	return cur

def test_connection():
	"""Tries to open and close a database connection."""

	conn = connection()
	conn.close()
	return True

def dbconnection(f):
	"""
	A decorator that provides a database connection and 
	a related cursor to the function as respective conn 
	and cur named parameters.

	"""

	@wraps(f)
	def connection_wrapper(*args, **kwargs):
		conn = connection()
		cur = cursor(conn) 
		kwargs['conn'] = conn
		kwargs['cur'] = cur 

		result = f(*args, **kwargs)

		cur.close()
		conn.close()
		return result
	return connection_wrapper
