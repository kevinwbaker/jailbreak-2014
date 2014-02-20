import datetime

from django.conf import settings

def static(request):
    ''' Add static URL to the context, including the revision number (if known) when not in DEBUG mode. '''
    if settings.DEBUG and settings.REVISION:
        static_url = u'%sv%s/' % (settings.STATIC_URL, settings.REVISION)
    else:
        static_url = settings.STATIC_URL
    return {'STATIC_URL': static_url}

def jailbreak_settings(request):
    # timer related stuff
    started = False
    seconds_to_start = (settings.START_TIME - datetime.datetime.now()).total_seconds()
    if seconds_to_start < 0:
        seconds_to_start = 0
        started = True

    return {
       'MAIN_SPONSOR_PAGE': settings.MAIN_SPONSOR_PAGE,
       'STARTED': started,
       'SECONDS_TO_START': seconds_to_start,
    }