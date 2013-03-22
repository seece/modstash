import os
import logging
import psycopg2

if not 'DATABASE_URL' in os.environ:
	raise Exception("No database URL!")
else:
	print("Database URL found.")

dburl = os.environ['DATABASE_URL']
schema = "ms"

def test_connection():
	try:
		conn = psycopg2.connect(dburl)
	except Exception as e:
		print("Database error: " + str(e))
		raise
	conn.close()
	return True

def get_connection():
	try:
		conn = psycopg2.connect(dburl)
	except Exception as e:
		print("Database error: " + str(e))
		raise
	return conn
