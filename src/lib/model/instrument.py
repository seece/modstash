import hashlib
from database import dbconnection
import lib.model.sample as Sample
import lib.model.samplehash as SampleHash
from lib.model.samplehash import NoSuchHashException


@dbconnection
def add_instrument(songid, ins, index, cur, conn):
	"""Adds an instrument to the database."""

	m = hashlib.md5(ins.sample.data)
	md5hash = m.hexdigest()
	name = ins.sample.name or ''

	sampleid = None

	try:
		sampleid = SampleHash.get_sample_id(md5hash, ins.sample.length)
	except NoSuchHashException as e:
		samplename = ins.sample.name or ''
		sampleid = Sample.add(samplename)
		SampleHash.add(md5hash, ins.sample.length, sampleid)

	query = """
			INSERT INTO Instrument 
			(sampleid, songid, index, name) 
			VALUES (%s, %s, %s, %s);
			"""

	try:
		cur.execute(query, (sampleid, songid, index, name))
	except Exception as e:
		print("Can't add instrument: %s" % (str(e)))
		raise

	conn.commit()


