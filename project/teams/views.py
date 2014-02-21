import datetime

from django.http import Http404
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from teams.models import Team, Checkin

def teams(request, template=None):
    '''Lists all the teams'''
    context = RequestContext(request)

    context['teams'] = Team.objects.all()
    return render_to_response(template, context_instance=context)

def team(request, slug, template=None):
    '''Full details for an team'''
    context = RequestContext(request)

    try:
        team = Team.objects.get(slug=slug)
    except Team.DoesNotExist:
        raise Http404

    context['team'] = team
    context['checkins'] = team.checkins.all()
    context['posts'] = team.posts.all()
    return render_to_response(template, context_instance=context)

def universities(request, template=None):
    '''All the universities compared and contrasted'''
    universities = []
    for key, name in Team.UNIVERSITIES:
        # get all the teams for this university
        teams = Team.objects.all().filter(university=key)

        # names
        name = name.upper()
        try:
            full_name = teams[0].university_full_name
        except IndexError:
            full_name = name

        # calculate stats
        total_raised = sum([team.amount_raised for team in teams])
        average_raised = total_raised/(len(teams) or 1)
        total_distance_from_start = int(sum([team.distance for team in teams]))
        average_distance_from_start = total_distance_from_start/(len(teams) or 1)

        universities.append({
                'name': name,
                'key': name.lower(),
                'full_name': full_name,
                'teams': teams,
                'stats': [
                    {
                        'name': "Number of Teams",
                        'value': "%d" % len(teams),
                    },
                    {
                        'name': "Total Amount Raised",
                        'value': "&euro; %d" % total_raised
                    },
                    {
                        'name': "Average Raised per Team",
                        'value': "&euro; %d" % average_raised,
                    },
                    {
                        'name': "Total Distance from Start",
                        'value': "%d km" % total_distance_from_start,
                    },
                    {
                        'name': "Average Distance from Start per Team",
                        'value': "%d km" % average_distance_from_start,
                    }
                ]
            })

        # find which university is the best
        best_travellers = None
        best_travellers_distance = 0
        best_raisers = None
        best_raisers_amount = 0

        for uni in universities:
            average_raised = sum([team.amount_raised for team in uni['teams']])/(len(uni['teams']) or 1)
            average_travelled = sum([team.distance for team in uni['teams']])/(len(uni['teams']) or 1)

            if average_travelled > best_travellers_distance:
                best_travellers = uni['full_name']
                best_travellers_distance = average_travelled
            
            if average_raised > best_raisers_amount:
                best_raisers = uni['full_name']
                best_raisers_amount = average_raised

    return render(request, template, {
            'universities': universities,
            'best_travellers': best_travellers,
            'best_travellers_distance': int(best_travellers_distance),
            'best_raisers': best_raisers,
            'best_raisers_amount': best_raisers_amount,
        })

def university(request, slug, template=None):
    '''Lists all the teams for a university and some university stats'''

    # find matching university id for slug
    uni_id = Team.university_key_to_value(slug)
    if uni_id is None:
        raise Http404

    # get a possibly empty list of teams
    teams = Team.objects.all().filter(university=uni_id)

    # names
    name = Team.UNIVERSITIES[uni_id][1].upper()
    try:
        full_name = teams[0].university_full_name
    except IndexError:
        full_name = name

    # calculate stats
    total_raised = sum([team.amount_raised for team in teams])
    average_raised = total_raised/(len(teams) or 1)
    total_distance_from_start = int(sum([team.distance for team in teams]))
    average_distance_from_start = total_distance_from_start/(len(teams) or 1)

    university = {
        'name': name,
        'key': name.lower(),
        'full_name': full_name,
        'teams': teams,
        'stats': [
            {
                'name': "Number of Teams",
                'value': "%d" % len(teams),
            },
            {
                'name': "Total Amount Raised",
                'value': "&euro; %d" % total_raised
            },
            {
                'name': "Average Raised per Team",
                'value': "&euro; %d" % average_raised,
            },
            {
                'name': "Total Distance from Start",
                'value': "%d km" % total_distance_from_start,
            },
            {
                'name': "Average Distance from Start per Team",
                'value': "%d km" % average_distance_from_start,
            }
        ]
    }

    return render(request, template, {
            'university': university,
        })
