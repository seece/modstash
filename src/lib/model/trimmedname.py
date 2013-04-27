from database import dbconnection


@dbconnection
def get_song_name(songid, conn, cur):
	"""Gets song information with the numeric song id."""
	query = "SELECT * FROM trimmedname \
			WHERE songid=%s;"
	
	cur.execute(query, (songid,))
	return cur.fetchone()


