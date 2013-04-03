from database import dbconnection


@dbconnection
def get_song_name(songid, conn, cur):
	query = "SELECT * FROM trimmedname \
			WHERE songid=%s;"
	
	cur.execute(query, (songid,))
	return cur.fetchone()


