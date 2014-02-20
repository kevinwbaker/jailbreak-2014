from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('accounts',
    url(r'^login',
        view='views.login',
        kwargs={'template':'login.html'},
        name='login'
    ),
    url(r'^logout$',
        view='views.logout',
        kwargs={'template':'logout.html'},
        name='logout'
    ),
)