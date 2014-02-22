import datetime

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, Http404

from teams.models import Team, Checkin
from feeds.models import Tweet
from utilities.utils import create_form

def home(request, template=None):
    '''Home page'''
    # Standings
    teams = Team.objects.prefetch_related('checkins').all()
    teams_sort_by_distance = sorted(teams, key=lambda x: x.distance, reverse=True)
    
    # Feed
    posts = []
    tweets = Tweet.objects.all().order_by('-time').select_related('team')[:40]
    for tweet in tweets:
        posts.append(('twitter', tweet))

    checkins = Checkin.objects.all().order_by('-time').select_related('team')[:40]
    for checkin in checkins:
        posts.append(('checkin', checkin))

    posts_sorted = sorted(posts, key=lambda x: x[1].time, reverse=True)

    # Stats
    total_amount_raised = sum([team.amount_raised for team in teams])
    total_distance_from_start = sum([team.distance for team in teams])

    return render(request, template, {
            'standings': teams_sort_by_distance,
            'posts': posts_sorted,
            'total_amount_raised': total_amount_raised,
            'total_distance_from_start': int(total_distance_from_start),
            'home_page': True
        })

def custom_500_error_view(request, template='500.html'):
    '''Error pages don't get a chance to run the context processors
    that are inserting values like STATIC_URL into the context so that
    the theme of the site works.
    '''
    return render(request, template, {
        'STATIC_URL': settings.STATIC_URL
    })

def customer_404_error_view(request, template='404.html'):
    return render(request, template, {
        'STATIC_URL': settings.STATIC_URL   
    })
    
