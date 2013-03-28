import cherrypy

'''The main controller class. '''
class Controller:
	def __init__(self):
		pass

	'''Renders a template with some parameters pulled from the active session'''
	def render(self, view, **params):
		username=cherrypy.session.get('username')
		logged_in = username!=None

		if not 'error_message' in params:
			params['error_message'] = ''

		params['flash'] = flash=cherrypy.session.get('flash')
		params['username'] = username
		params['logged_in'] = logged_in
		return view.render(**params)

