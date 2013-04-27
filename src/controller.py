import cherrypy
import lib.model.user as User

class Controller:
	"""The main controller class. """
	def __init__(self):
		pass

	def render(self, view, **params):
		"""Renders a template with some parameters pulled from the active session"""
		username=cherrypy.session.get('username')
		logged_in = username!=None

		if not 'error_message' in params:
			params['error_message'] = ''

		try:
			current_user = cherrypy.session.get('username')
			user = User.get_user(username)
			
			params['member_type'] = user['member_type']
		except Exception as e:
			params['member_type'] = ''

		params['flash'] = flash=cherrypy.session.get('flash')
		params['username'] = username
		params['logged_in'] = logged_in
		return view.render(**params)

