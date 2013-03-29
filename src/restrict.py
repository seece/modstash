import cherrypy

def restrictfunc(group='member'):
	if not cherrypy.session.get('username'):
		raise cherrypy.HTTPError('401 Unauthorized')

	if group == 'member':
		return
	elif group == 'admin':
		# TODO actually pull the user information from the DB and check status
		return

# a custom authentication tool
restrict = cherrypy.Tool('before_handler', restrictfunc)

