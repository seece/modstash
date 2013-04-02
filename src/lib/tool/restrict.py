from functools import wraps
import cherrypy

def restrictfunc(group='member', method=None):
	if not cherrypy.session.get('username'):
		raise cherrypy.HTTPError('401 Unauthorized')

	if method:
		if cherrypy.request.method != method:
			raise cherrypy.HTTPError(404) # TODO return 405 and a list of allowed methods
		
	if group == 'member':
		return
	elif group == 'admin':
		# TODO actually pull the user information from the DB and check status
		return

# a custom authentication tool
restrict = cherrypy.Tool('before_handler', restrictfunc)
