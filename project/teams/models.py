import datetime
from decimal import Decimal
from math import sin, cos, sqrt, atan2, radians

from django.db import models
from django.conf import settings
from django_boto.s3.storage import S3Storage

from utilities.utils.memoize import memoize_instance

s3 = S3Storage()

class Team(models.Model):
    '''Team taking part'''

    TCD = 0
    NUIG = 1
    UCC = 2
    UCD = 3
    UNIVERSITIES = (
        (TCD, 'tcd'),
        (NUIG, 'nuig'),
        (UCC, 'ucc'),
        (UCD, 'ucd'),
    )

    STARTING_LAT = (
        (Decimal(settings.DUBLIN_START_LAT), "Dublin"),
        (Decimal(settings.CORK_START_LAT), "Cork"),
        (Decimal(settings.GALWAY_START_LAT), "Galway")
    )

    STARTING_LNG = (
        (Decimal(settings.DUBLIN_START_LNG), "Dublin"),
        (Decimal(settings.CORK_START_LNG), "Cork"),
        (Decimal(settings.GALWAY_START_LNG), "Galway")
    )

    number = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    photo = models.FileField(storage=s3, upload_to='jailbreak14-uploads', blank=True, null=True)
    sponsor_link = models.URLField()
    youtube_embed_link = models.URLField(null=True, help_text="Embed link of the team's application video")

    description = models.CharField(max_length=255, blank=True)
    amount_raised = models.IntegerField(default=200)
    university = models.PositiveSmallIntegerField(db_index=True, choices=UNIVERSITIES, default=TCD)
    
    start_lat = models.DecimalField(max_digits=8, decimal_places=4, default=settings.DUBLIN_START_LAT, choices=STARTING_LAT)
    start_lng = models.DecimalField(max_digits=8, decimal_places=4, default=settings.DUBLIN_START_LNG, choices=STARTING_LNG)

    @classmethod
    def university_key_to_value(cls, search):
        for value, key in cls.UNIVERSITIES:
            if key == search:
                return value

        return None

    @property
    def university_key(self):
        return self.UNIVERSITIES[self.university][1]

    @property
    def university_name(self):
        return self.UNIVERSITIES[self.university][1].upper()

    @property
    def university_full_name(self):
        if self.university is 0:
            return "Trinity College Dublin"
        elif self.university is 1:
            return "National University of Ireland, Galway"
        elif self.university == 2:
            return "University College Cork"
        elif self.university == 3:
            return "University College Dublin"

    @property
    def photo_url(self):
        if not self.photo:
            return settings.DEFAULT_PROFILER

        print "*****"
        print settings.UPLOADS_URL
        print self.photo
        print "URL: %s%s " % (settings.UPLOADS_URL, self.photo)

        return "%s%s" % (settings.UPLOADS_URL, self.photo)
    
    @property
    @memoize_instance
    def last_checkin(self):
        try:
            return self.checkins.latest('time')
        except Checkin.DoesNotExist:
            return None
    
    @property
    @memoize_instance
    def distance(self):
        '''The distance between the team (based on their last checkin) and the start pt'''
        if not self.last_checkin:
            return 0

        lat1 = radians(self.start_lat)
        lon1 = radians(self.start_lng)
        lat2 = radians(self.last_checkin.lat_position)
        lon2 = radians(self.last_checkin.lng_position)

        return world_distance(lat1, lon1, lat2, lon2)

    @property
    @memoize_instance
    def distance_travelled(self):
        print "HEY"
        travelled = 0
        lat1 = radians(self.start_lat)
        lon1 = radians(self.start_lng)

        print self.checkins.all()

        for checkin in self.checkins.all():
            lat2 = radians(checkin.lat_position)
            lon2 = radians(checkin.lng_position)

            travelled += world_distance(lat1, lon1, lat2, lon2)
            print "T: ", travelled

            lat1 = lat2
            lon1 = lon2
    
        return travelled

    def __unicode__(self):
        return "{university}: {number} - {name}".format(name=self.name, number=self.number, university=self.university_name)

class Checkin(models.Model):
    '''Locations the team has checked in at'''

    name = models.CharField(max_length=255, help_text="A useful name for the location where they checked in")
    message = models.TextField(null=True, help_text="A nice message from the team or about thier journey to this checkin point")
    lng_position = models.DecimalField(max_digits=8, decimal_places=4)
    lat_position = models.DecimalField(max_digits=8, decimal_places=4)
    team = models.ForeignKey('Team', related_name='checkins')
    time = models.DateTimeField(default=datetime.datetime.utcnow)

    def __unicode__(self):
        return "Checkin in from {team} at {name})".format(team=self.team, name=self.name)

def world_distance(lat1, lon1, lat2, lon2):
    '''Calculates the distance between two sets of GPS coordinates'''
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = settings.RADIUS_EARTH * c

    return distance
