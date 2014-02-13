from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('teams',
    url(r'^$',
        view='views.teams',
        kwargs={'template':'teams.html'},
        name='teams'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
    	view='views.team',
    	kwargs={'template':'team.html'},
    	name='team'
    )
)