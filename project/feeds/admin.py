from django.contrib import admin

from feeds.models import TwitterStream, Tweet

admin.site.register(TwitterStream)
admin.site.register(Tweet)
