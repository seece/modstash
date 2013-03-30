import unittest
from mako.template import Template
from model.user import User

class TemplateTests(unittest.TestCase):
	def setUp(self):
		pass

	def test_inline_render(self):
		templ = Template("test: ${x}")
		render = templ.render(x=5)
		self.assertEquals("test: 5", render)
