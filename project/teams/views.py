import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from teams.models import Team

def teams(request, template=None):
    '''Lists all the teams'''
    context = RequestContext(request)

    context['teams'] = Team.objects.all()

    context['teams_listing_page'] = True
    return render_to_response(template, context_instance=context)

def team(request, slug, template=None):
    '''Full details for an team'''
    context = RequestContext(request)

    context['team'] = get_object_or_404(Team, slug=slug)

    context['team_page'] = True
    return render_to_response(template, context_instance=context)

@staff_member_required
def add_checkin(request, template=None):
    '''Allow staff to add a new checkin for a team'''
    pass