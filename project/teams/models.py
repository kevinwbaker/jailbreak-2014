import datetime
from math import sin, cos, sqrt, atan2, radians

from django.db import models
from django.conf import settings
from utilities.utils.memoize import memoize_instance

class Team(models.Model):
    '''Team taking part'''

    TCD = 0
    NUIG = 1
    UCC = 2
    UCD = 3
    UNIVERSITIES = (
        (TCD, 'tcd', "Trinity College Dublin"),
        (NUIG, 'nuig', "National University of Ireland, Galway"),
        (UCC, 'ucc', "University College Cork"),
        (UCD, 'ucd', "University College Dublin"),
    )
    
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    photo = models.FileField(upload_to='teams')
    sponsor_link = models.URLField()
    description = models.CharField(max_length=255)
    amount_raised = models.IntegerField(default=0)
    university = models.PositiveSmallIntegerField(db_index=True)

    @property
    def university_name(self):
        return self.UNIVERSITIES[self.university][1]

    @property
    def university_full_name(self):
        return self.UNIVERSITIES[self.university][2]
    
    @property
    @memoize_instance
    def last_checkin(self):
        try:
            return self.checkins.latest('time')
        except Checkin.DoesNotExist:
            return None
    
    @property
    def distance(self):
        '''The distance between the team (based on their last checkin) and the start pt'''
        if not self.last_checkin:
            return 0

        lat1 = radians(settings.START_LAT)
        lon1 = radians(settings.START_LNG)
        lat2 = radians(self.last_checkin.lat_position)
        lon2 = radians(self.last_checkin.lng_position)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = settings.RADIUS_EARTH * c

        return distance

    def __unicode__(self):
        return "{university}: {number} - {name}".format(name=self.name, number=self.number, university=self.university_name.upper())

class Checkin(models.Model):
    '''Locations the team has checked in at'''

    name = models.CharField(max_length=255, help_text="A useful name for the location where they checked in")
    lng_position = models.DecimalField(max_digits=8, decimal_places=3)
    lat_position = models.DecimalField(max_digits=8, decimal_places=3)
    team = models.ForeignKey('Team', related_name='checkins')
    time = models.DateTimeField(default=datetime.datetime.utcnow)

    def __unicode__(self):
        return "Checkin in from {team} at {name})".format(team=self.team, name=self.name, )


