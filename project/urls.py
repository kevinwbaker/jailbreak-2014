from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        view='accounts.views.home',
        kwargs={'template':'home.html'},
        name='home'
    ),
    (r'^accounts/', include('accounts.urls')),
    (r'^teams/', include('teams.urls')),
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += patterns('django.contrib.flatpages.views',
    (r'^pages/(?P<url>.*/)$', 'flatpage'),
)

# In debug mode, static files are automatically served by Django.
# Also serve user-uploaded files.
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % settings.UPLOADS_DIRNAME,
            'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
            }
        ),
        url(r'^%(MEDIA_URL)s/(?P<path>.*)$' % {'MEDIA_URL': settings.MEDIA_URL.strip('/')},
            'django.views.static.serve',
            { 'document_root': settings.MEDIA_ROOT }),
   )
