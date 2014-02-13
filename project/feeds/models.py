from django.db import models

class Feed(models.Model):
	'''Social media feed we want to pull in for this team'''

	TWITTER = 'twitter'
    FACEBOOK_PAGE = 'fb_page'
    SOURCES = (
        (TWITTER, 'Twitter'),
        (FACEBOOK_PAGE, 'Facebook Page'),
    )
	source = models.CharField(max_length=10, choices=SOURCES)
	feed_id = models.CharField(max_length=128)

	def __unicode__(self):
		return "{source}: {feed_id}".format(source=SOURCES[self.source], feed_id=feed_id)

class Post(models.Model):
	'''A post from a social media feed'''

	message = models.TextField()