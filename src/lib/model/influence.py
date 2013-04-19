from database import dbconnection

class Influence:
	"""The Influence database model."""

	@classmethod
	@dbconnection
	def add_internal_influence(cls, source_id, destination_id, inf_type, conn, cur):
		index = 0

		query = "INSERT INTO influence \
				(source_id, destination_id, index, external_url, type) \
				VALUES (%s, %s, %s, %s, %s);"

		try:
			cur.execute(query, (
					source_id,
					destination_id,
					index,
					None,
					inf_type))
			conn.commit()

		except Exception as e:
			print("Can't add influence: " + str(e))
			raise

	@classmethod
	@dbconnection
	def get_song_id_from_url(cls, url, conn, cur):
		#TODO add proper url parsing
		return 8
