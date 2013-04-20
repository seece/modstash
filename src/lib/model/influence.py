from urllib.parse import urlparse
from lib.model.song import Song
from database import dbconnection

class InvalidSongUrlException(Exception):
	"""Thrown if get_song_id_from_url is given a malformed url."""
	pass

class Influence:
	"""The Influence database model."""

	@classmethod
	@dbconnection
	def add_internal_influence(cls, source_id, destination_id, inf_type, conn, cur):
		"""Adds an internal influence to the database."""
		index = 0

		query = """INSERT INTO influence 
				(source_id, destination_id, index, external_url, type) 
				VALUES (%s, %s, %s, %s, %s);"""

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
		"""Parses a given song url and returns a song id."""
		obj = urlparse(url)
		parts = obj.path.split('/')

		if parts[1] != 'songs':
			raise InvalidSongUrlException()

		if len(parts) < 4:
			raise InvalidSongUrlException()

		owner = parts[2]
		trimmed_name = parts[3]
		return Song.get_id_by_trimmedname(owner, trimmed_name)

	@classmethod
	@dbconnection
	def get_song_influences(cls, songid, conn, cur):
		query = """	SELECT songid, nicename, index, type, title, owner
					FROM influence 
					INNER JOIN trimmedname ON source_id = songid 
					INNER JOIN song ON id = source_id 
					AND destination_id = %s
					ORDER BY index ASC;
				"""

		cur.execute(query, (songid,))
		result = cur.fetchall()

		return result


