import datetime

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, Http404

from teams.models import Team
from feeds.models import Post
from accounts.forms import EmailAuthenticationForm
from utilities.utils import create_form

def home(request, template=None):
    '''Home page'''
    # Standings
    teams = Team.objects.all()
    teams_sort_by_distance = sorted(teams, key=lambda x: x.distance, reverse=True)
    
    # Feed
    posts = Post.objects.all().order_by('-time').select_related('team')

    # Stats
    total_amount_raised = sum([team.amount_raised for team in teams])
    total_distance_from_start = sum([team.distance for team in teams])

    return render(request, template, {
            'standings': teams_sort_by_distance,
            'posts': posts,
            'total_amount_raised': total_amount_raised,
            'total_distance_from_start': int(total_distance_from_start),
            'home_page': True
        })

def login(request, template=None):
    '''User login page'''

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    login_form = create_form(EmailAuthenticationForm, request, request)
    if request.method == 'POST':
        if login_form.is_valid():
            return HttpResponseRedirect(r'/')

    return render(request, template, {
            'login_form': login_form,
            'login_page': True
        })

@login_required
def logout(request, template=None):
    '''User logout page'''
    auth_logout(request)

    return render(request, template, {
            'logout_page': True
        })
