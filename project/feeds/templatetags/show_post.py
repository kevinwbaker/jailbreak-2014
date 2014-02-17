from django import template
from django.template import loader, TemplateDoesNotExist

register = template.Library()

@register.simple_tag(takes_context=True)
def show_post(context, post):
	'''Selects the correct template to show this post object with and
	renders the post object using that template
	'''
	try:
		t = loader.get_template(post.source_key + '.html')
	except TemplateDoesNotExist:
		return ''

	return t.render(context)