from database import dbconnection

class Sample:
	"""The Sample model."""

	@classmethod
	@dbconnection
	def add(cls, samplename, conn, cur):
		"""Adds a new sample to the DB. 
		Returns the added id."""

		query = "INSERT INTO sample (name) \
				VALUES (%s) RETURNING id;"

		try:
			cur.execute(query, (samplename,))
		except Exception as e:
			print("Can't add Sample: %s" % (str(e)))
			raise

		conn.commit()
		return cur.fetchone()['id']


