
from mako.template import Template
from mako.lookup import TemplateLookup


class View():
	template_lookup = TemplateLookup(directories=['templates'])

	public_config = {'title': 'modstash', 
			'stylepath' : '/static/css/style.css'}

	'''Initializes a new View from the given template path'''
	def __init__(self, path):
		self.path = path
		self.template = Template(filename=path, output_encoding='utf-8', lookup=self.template_lookup) 

	'''Renders the view with the given arguments.
	The public configuration is added to the named argument dict.'''
	def render(self, **params):
		params['config'] = self.public_config
		params['state'] = {}
		return self.template.render(**params)


index_view = View('templates/index.html')
