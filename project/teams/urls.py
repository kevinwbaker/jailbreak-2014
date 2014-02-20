from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('teams',
    url(r'^teams/$',
        view='views.teams',
        kwargs={'template':'teams.html'},
        name='teams'
    ),
    url(r'^teams/(?P<slug>[\w-]+)/$',
    	view='views.team',
    	kwargs={'template':'team.html'},
    	name='team'
    ),
    url(r'^universities/challenges/$',
        view='views.universities',
        kwargs={'template':'universities.html'},
        name='universities'
    ),
    url(r'^universities/(?P<slug>[\w-]+)/$',
        view='views.university',
        kwargs={'template':'university.html'},
        name='university'
    ),
)