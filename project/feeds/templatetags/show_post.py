from django import template
from django.template import loader, TemplateDoesNotExist

register = template.Library()

@register.simple_tag(name='show_post', takes_context=True)
def show_post(context, type_, post):
	'''Selects the correct template to show this post object with and
	renders the post object using that template
	'''
	try:
		t = loader.get_template(type_ + '.html')
	except TemplateDoesNotExist:
		return ''

	return t.render(context)