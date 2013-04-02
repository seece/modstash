import hashlib
from lib.model.sample import *
from lib.model.samplehash import *


class Instrument:
	"""The Instrument model."""

	@classmethod
	@dbconnection
	def add_instrument(cls, songid, ins, index, cur, conn):
		m = hashlib.md5(ins.sample.data)
		md5hash = m.hexdigest()
		#print("INST: " + str(i.sample.name) + " = " + samplehash + " is " + str(i.sample.length))
		name = ins.sample.name or ''

		sampleid = None

		try:
			sampleid = SampleHash.get_sample_id(md5hash, ins.sample.length)
		except NoSuchHashException as e:
			samplename = ins.sample.name or ''
			sampleid = Sample.add(samplename)
			SampleHash.add(md5hash, ins.sample.length, sampleid)

		query = "INSERT INTO Instrument \
				(sampleid, songid, index, name) \
				VALUES (%s, %s, %s, %s);"

		try:
			cur.execute(query, (sampleid, songid, index, name))
		except Exception as e:
			print("Can't add instrument: %s" % (str(e)))
			raise

		conn.commit()


