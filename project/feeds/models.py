import datetime

from django.db import models

class Feed(models.Model):
    '''A social media feed belonging to a team

    Each team can have multiple feeds for each source.
    '''

    TWITTER = 0
    TWITTER_LIST = 1
    FACEBOOK_PAGE = 2
    SOURCES = (
        (TWITTER, 'Twitter'),
        (TWITTER_LIST, 'Twitter List'),
        (FACEBOOK_PAGE, 'Facebook Page'),
    )
    source = models.PositiveSmallIntegerField()
    feed_id = models.CharField(max_length=128)
    team = models.ForeignKey('teams.Team', related_name='feeds', null=True)

    @property
    def source_name(self):
        return self.SOURCES[self.soruce][1]

    @property
    def has_team(self):
        return self.team is not None

    def __unicode__(self):
        return "{source}: {feed_id}".format(source=SOURCES[self.source], feed_id=feed_id)

class Post(models.Model):
    '''
    A post from a social media or custom feed.

    This post does not need to belong to a team as it can 
    contain messages from the system for example if a new event
    we want to publise occurs.
    '''
    MANUAL = 0
    CHECKIN = 1
    TWITTER = 2
    FACEBOOK_PAGE = 3
    SOURCES = (
        (MANUAL, 'manual', "Manual"),
        (CHECKIN, 'checkin', "Checkin"),
        (TWITTER, 'twitter', "Twitter"),
        (FACEBOOK_PAGE, 'facebook', "Facebook Page"),
    )
    source = models.PositiveSmallIntegerField()

    url = models.URLField(null=True) # where was the original message
    media = models.URLField(null=True)
    message = models.TextField() # html of the message
    time = models.DateTimeField(default=datetime.datetime.utcnow)
    
    # user of the social media who posted it
    user = models.CharField(max_length=250, null=True)
    user_photo = models.URLField(null=True) # url to where the message is hosted
    user_url = models.URLField(null=True)
    
    team = models.ForeignKey('teams.Team', related_name='posts', null=True)

    @property
    def source_key(self):
        return self.SOURCES[self.source][1]

    @property
    def source_name(self):
        return self.SOURCES[self.source][2]

    @property
    def has_media(self):
        return self.media is not None

    @property
    def has_team(self):
        return self.team is not None
    

