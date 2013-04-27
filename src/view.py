
import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup


def make_song_url(username, trimmed_name):
	"""
	Transforms a username and song identification name
	to a proper absolute url.

	Used by the template rendering functions.
	"""

	return "/songs/%s/%s" % (username, trimmed_name)

class View():
	"""A thin wrapper around a Mako Template. Adds some settings to the render parameters."""
	template_lookup = TemplateLookup(directories=['templates'])

	public_config = {'title': 'modstash', 
			'stylepath' : '/static/css/style.css',
			'dateformat' : '%Y.%m.%d %H:%M' }

	def __init__(self, path):
		"""Initializes a new View from the given template path"""
		self.path = path
		self.template = Template(filename=path, output_encoding='utf-8', lookup=self.template_lookup) 


	def render(self, **params):
		"""Renders the view with the given arguments.
		The public configuration is added to the named argument dict."""

		params['config'] = self.public_config
		params['make_song_url'] = make_song_url

		return self.template.render(**params)


index_view 		= View('templates/index.html')
user_view 		= View('templates/user.html')
error_view 		= View('templates/error.html')
upload_view 	= View('templates/upload.html')
song_view 		= View('templates/song.html')
register_view 	= View('templates/register.html')
sample_view 	= View('templates/sample.html')
login_view		= View('templates/login.html')
