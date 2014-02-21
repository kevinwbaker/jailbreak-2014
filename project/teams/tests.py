from math import radians
from decimal import Decimal

from django.conf import settings
from django.core.urlresolvers import reverse

from teams.models import Team, Checkin, world_distance
from utilities.utils import CleanTestCase

class TeamModelTest(CleanTestCase):
	'''
	Tests the methods of the Team model class

	Team 1 has multiple checkins
	Team 2 has one checkin
	Team 3 has no checkins
	'''

	fixtures = [
		'teams.json',
		'checkins.json'
	]

	def test_last_checkin(self):
		'''Test Team.last_checkin()'''
		team1 = Team.objects.get(pk=1)
		self.assertEqual(team1.last_checkin.pk, 8)

		team3 = Team.objects.get(pk=3)
		self.assertIsNone(team3.last_checkin)

	def test_world_distance(self):
		'''Tests teams.models.world_distance() a common
		function for calculating the distance between two
		GPS coordinates.
		'''
		dublin_lat = radians(Decimal("53.3418"))
		dublin_lng = radians(Decimal("-6.3098"))

		galway_lat = radians(Decimal("53.2741"))
		galway_lng = radians(Decimal("-9.0498"))

		# same point twice
		result = world_distance(dublin_lat, dublin_lng, dublin_lat, dublin_lng)
		self.assertEqual(result, 0)

		# Dublin to Galway
		result = world_distance(dublin_lat, dublin_lng, galway_lat, galway_lng)
		self.assertAlmostEqual(182.248, result, places=2)

	def test_distance(self):
		'''Tests Team.distance property on Team object'''
		team1 = Team.objects.get(pk=1)
		self.assertAlmostEqual(5917, team1.distance, places=0)

		team2 = Team.objects.get(pk=2)
		self.assertAlmostEqual(464, team2.distance, places=0)

		team3 = Team.objects.get(pk=3)
		self.assertEqual(0, team3.distance)

	def test_distance_travelled(self):
		'''Tests Team.distance_travelled property on Team object'''
		team1 = Team.objects.get(pk=1)
		self.assertAlmostEqual(6100, team1.distance_travelled, places=0)

		team2 = Team.objects.get(pk=2)
		self.assertAlmostEqual(464, team2.distance_travelled, places=0)

		team3 = Team.objects.get(pk=3)
		self.assertEqual(0, team3.distance_travelled)

	def test_unicode(self):
		'''Test the __unicode__ method on Team'''
		team = Team.objects.get(pk=1)
		self.assertIsNotNone(unicode(team))

class CheckinModelTest(CleanTestCase):
	fixtures = [
		'teams.json',
		'checkins.json'
	]

	def test_unicode(self):
		'''Test the __unicode__ method on Checkin'''
		checkin = Checkin.objects.get(pk=1)
		self.assertIsNotNone(unicode(checkin))

class TeamViewTest(CleanTestCase):
    '''Tests the team profile view page'''

    fixtures = [
        'teams.json',
    ]

    def test_404(self):
        '''Tests that polling a non existing Team returns a 404'''
        resp = self.client.get(reverse('team', args=['999']))
        self.assertEqual(resp.status_code, 404)

    def test_200(self):
        '''Tests that when we request a Team that exists we get a 200 response'''
        resp = self.client.get(reverse('team', args=['peter-sean']))
        self.assertEqual(resp.status_code, 200)

        # test the returned context makes some sense
        self.assertIn('team', resp.context)
        self.assertEqual(resp.context['team'].pk, 1)

class TeamsViewTest(CleanTestCase):
    '''Tests the teams listing page'''

    fixtures = [
        'teams.json',
    ]

    def test_200(self):
        '''Tests that when we request a Team that exists we get a 200 response'''
        resp = self.client.get(reverse('teams'))
        self.assertEqual(resp.status_code, 200)

        # test the returned context makes some sense
        self.assertIn('teams', resp.context)
