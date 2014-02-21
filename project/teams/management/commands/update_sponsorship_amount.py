import bs4
import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core import management

from teams.models import Team

def get_amount_raised(url):
    '''
    Polls the webpage and attempts to extract the amount of money
    the team has raised thus far.

    Returns
        int - success
        boolean False - couldn't extract the value
    '''
    # pull page
    r = requests.get(url)
    page = r.text

    # extract links out 
    soup = bs4.BeautifulSoup(page)

    values = soup.find_all('h2', {'class': 'nb'})

    for val in values:
        try:
            return int(val.text.strip().replace(',', ''))
        except ValueError:
            pass

    return False

class Command(BaseCommand):

    def handle(self, *args, **options):
        '''For each Team object check their sponsorship
        page and update their record in the database
        '''
        teams = Team.objects.all()

        for team in teams:
            raised = get_amount_raised(team.sponsor_link)
            if raised:
                print "Updating amount for {team} from {previous} to {new}".format(team=team, previous=team.amount_raised, new=raised)
                team.amount_raised = raised
                team.save()
            else:
                print "Unable to update the amount for {team}".format(team=team)
    
