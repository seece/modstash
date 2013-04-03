
import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup

'''A thin wrapper around a mako Template. Adds some settings to the render parameters.'''
class View():
	template_lookup = TemplateLookup(directories=['templates'])

	public_config = {'title': 'modstash', 
			'stylepath' : '/static/css/style.css',
			'dateformat' : '%Y.%m.%d %H:%M' }

	'''Initializes a new View from the given template path'''
	def __init__(self, path):
		self.path = path
		self.template = Template(filename=path, output_encoding='utf-8', lookup=self.template_lookup) 

	'''Renders the view with the given arguments.
	The public configuration is added to the named argument dict.'''
	def render(self, **params):
		params['config'] = self.public_config
		#params['state'] = {}

		return self.template.render(**params)


index_view = View('templates/index.html')
user_view = View('templates/user.html')
error_view = View('templates/error.html')
upload_view = View('templates/upload.html')
song_view = View('templates/song.html')
register_view = View('templates/register.html')
sample_view = View('templates/sample.html')
