import unittest
import database
from model.user import UserModel

class DatabaseTests(unittest.TestCase):
	def setUp(self):
		try:
			self.conn = database.connection()
		except Exception as e:
			raise

	def tearDown(self):
		self.conn.close()

	'''
	def test_connection(self):
		try:
			conn = database.connection()
		except Exception as e:
			raise

		conn.close()
	'''

	def test_cursor(self):
		try:
			cur = database.cursor(self.conn)
		except Exception as e:
			raise

		cur.close()

	def test_tables_exist(self):
		try:
			cur = database.cursor(self.conn)
		except Exception as e:
			raise

		names = ['member', 'author', 'song', 'trimmedname', 'influence',
				'instrument', 'sample', 'samplehash']

		for name in names:
			cur.execute("select * from information_schema.tables where table_name=%s", (name,))
			self.assertTrue(cur.rowcount > 0, "table not found: " + name)

		cur.close()
