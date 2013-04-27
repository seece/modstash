from database import dbconnection

class NoSuchHashException(Exception):
	pass

@dbconnection
def get_sample_id(samplehash, filesize, conn, cur):
	"""Fetch the sample id with the matching MD5 hash."""

	query = """
			SELECT * FROM SampleHash 
			WHERE hash = %s AND filesize = %s;
			"""

	try:
		cur.execute(query, (samplehash, filesize))
	except Exception as e:
		print("Cannot search SampleHash: %s" % (str(e)))

	if cur.rowcount == 0:
		raise NoSuchHashException()

	return cur.fetchone()['sampleid']

@dbconnection
def add(md5hash, filesize, sampleid, conn, cur):
	"""Adds a new hash to the database."""
	
	query = """
			INSERT INTO SampleHash 
			(sampleid, hash, filesize) 
			VALUES (%s, %s, %s);
			"""

	try:
		cur.execute(query, (sampleid, md5hash, filesize))
	except Exception as e:
		print("Cannot insert SampleHash: %s" % (str(e)))
		raise

	conn.commit()



	

