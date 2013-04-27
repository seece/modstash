from functools import wraps
import cherrypy
from lib.flash import flash

def restrictfunc(group='member', method=None):
	"""
	An authentication function used to create a simple
	CherryPy compatible tool decorator.

	Checks if the current session satisfied the given
	conditions, if not the user is directed to a login page.
	"""

	if not cherrypy.session.get('username'):
		#raise cherrypy.HTTPError('401 Unauthorized')
		flash(restrict.error_message)
		raise cherrypy.HTTPRedirect(restrict.loginpath)

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
restrict.loginpath = "/loginform"
restrict.error_message = "You must log in to access this page."
