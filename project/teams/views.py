import datetime

from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
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

def universities(request, template=None):
    '''All the universities compared and contrasted'''
    universities = []
    for key, name, full_name in Team.UNIVERSITIES:
        # get all the teams for this university
        teams = Team.objects.all().filter(university=key)

        # calculate stats
        total_raised = sum([team.amount_raised for team in teams])
        average_raised = total_raised/len(teams)
        total_distance_from_start = int(sum([team.distance for team in teams]))
        average_distance_from_start = total_distance_from_start/len(teams)

        universities.append({
                'name': name,
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

        # find which university is the bests
        best_travellers = None
        best_travellers_distance = 0
        best_raisers = None
        best_raisers_amount = 0

        for uni in universities:
            average_raised = sum([team.amount_raised for team in uni['teams']])/len(uni['teams'])
            average_travelled = sum([team.distance for team in uni['teams']])/len(uni['teams'])

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
            'universities_page': True
        })

def university(request, slug, template=None):
    '''Lists all the teams for a university and some university stats'''

    return render(request, template, {
            'university_page': True
        })

@login_required
def edit_team(request, template=None):
    '''View to allow teams edit their details'''
    context = RequestContext(request)

    if request.method == 'POST':
        pass

    return render_to_response(template, context_instance=context)

@staff_member_required
def add_checkin(request, template=None):
    '''Allow staff to add a new checkin for a team'''
    context = RequestContext(request)

    return render_to_response(template, context_instance=context)
