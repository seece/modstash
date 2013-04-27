from database import dbconnection
import lib.model.user as User
import lib.model.trimmedname as TrimmedName

@dbconnection
def add(samplename, conn, cur):
	"""
	Adds a new sample to the DB. 
	Returns the added id.
	"""

	query = "INSERT INTO sample (name) \
			VALUES (%s) RETURNING id;"

	try:
		cur.execute(query, (samplename,))
	except Exception as e:
		print("Can't add Sample: %s" % (str(e)))
		raise

	conn.commit()
	return cur.fetchone()['id']

@dbconnection
def get_sample_songs(sampleid, conn, cur):
	"""
	Fetches all songs that use this sample.
	Sorted newest first. Also adds in the 'nicename'
	field.
	"""

	query = "SELECT DISTINCT * FROM song, trimmedname WHERE \
			song.id in \
				(SELECT songid FROM instrument \
				WHERE sampleid = %s) \
			AND song.id = trimmedname.songid \
			ORDER BY upload_date DESC;"

	try:
		cur.execute(query, (sampleid,))
	except Exception as e:
		print("Can't find sample songs: %s" % (str(e)))
		raise

	result = cur.fetchall()

	return result

@dbconnection
def get_name(sampleid, conn, cur):
	"""Gets the plaintext sample name."""
	query = "SELECT * FROM sample WHERE \
			sample.id = %s;"

	try:
		cur.execute(query, (sampleid,))
	except Exception as e:
		print("Can't find sample: %s" % (str(e)))
		raise

	result = cur.fetchone()

	if not result:
		print("No sample name for %s." % sampleid)
		return None

	return result['name']



