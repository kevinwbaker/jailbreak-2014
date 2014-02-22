import datetime

from django.db import models
from django.utils.html import strip_tags

class TwitterStream(models.Model):
    '''A Twitter statuses stream.

    May or may not belong to a team.
    '''

    TWITTER = 0
    TWITTER_LIST = 1
    TYPES = (
        (TWITTER, 'Twitter'),
        (TWITTER_LIST, 'Twitter List'),
    )
    type = models.PositiveSmallIntegerField()
    stream_id = models.BigIntegerField(max_length=128)
    include_rts = models.BooleanField(default=False)
    label = models.CharField(max_length=100, help_text="A label to easily identify streams")
    team = models.ForeignKey('teams.Team', related_name='feeds', blank=True, null=True)

    @property
    def type_name(self):
        return self.TYPES[self.type][1]

    @property
    def has_team(self):
        return self.team is not None

    def __unicode__(self):
        return "{type}: ({stream_id}) {label} (include rts: {include})".format(type=self.type_name, stream_id=self.stream_id, label=self.label, include=self.include_rts)


class Tweet(models.Model):
    '''A tweet from Twitter'''

    tweet_id = models.CharField(unique=True, max_length=25)
    media_url = models.URLField(blank=True, null=True)
    message = models.TextField()  # even though it is a tweet the message contains HTML that might make it more than 140 chars
    time = models.DateTimeField(default=datetime.datetime.utcnow)

    in_reply_to_user_name = models.CharField(max_length=250, blank=True, null=True)
    retweeted = models.BooleanField(default=False)
    
    # user of the social media who posted it
    user_name = models.CharField(max_length=250)
    user_photo = models.URLField() # url to where the message is hosted
    user_id = models.CharField(max_length=25)

    team = models.ForeignKey('teams.Team', related_name='tweets', blank=True, null=True)

    @property
    def tweet_url(self):
        '''Builds the URL to the original tweet on Twitter.com'''
        return 'http://twitter.com/{username}/status/{tweet_id}'.format(tweet_id=self.tweet_id, username=self.user_name)

    @property
    def user_url(self):
        '''Builds the URL to the users profile on Twitter.com'''
        return 'http://twitter.com/{username}'.format(username=self.user_name)


    @property
    def has_media(self):
        return self.media_url is not None

    @property
    def has_team(self):
        return self.team is not None

    def __unicode__(self):
        return "Tweet: {user_name} {message}...".format(user_name=self.user_name, message=strip_tags(self.message)[:100])  

