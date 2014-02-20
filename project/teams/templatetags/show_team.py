from django import template
from django.template import loader, TemplateDoesNotExist

register = template.Library()

@register.simple_tag(name='show_team', takes_context=True)
def show_team(context, team):
	'''Selects the correct template to show this post object with and
	renders the post object using that template
	'''
	try:
		t = loader.get_template('card.html')
	except TemplateDoesNotExist:
		return '<li>Failed to load details for team %s</li>' % team.name

	return t.render(context)