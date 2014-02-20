import os
import datetime

DIRNAME = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))

DEBUG = False 

if int(os.environ.get('DJANGO_DEBUG', "1")) is 1:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG
REVISION = "v1"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# While debugging, use the built-in server's static file serving mechanism.
# In production, host all files on S3.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.herokuapp.com').split(':')

if not DEBUG:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
    
    # Access information for the S3 bucket
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STATIC_BUCKET_NAME = os.environ['AWS_STATIC_BUCKET_NAME']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_UPLOADS_BUCKET_NAME']
    BOTO_S3_BUCKET = os.environ['AWS_STATIC_BUCKET_NAME']
    #AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME

    # Make this unique, and don't share it with anybody.
    #SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

    # Static files are stored in the bucket at /static
    # and user-uploaded files are stored at /media
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media'
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    STATIC_S3_PATH = 'static'
    AWS_S3_SECURE_URLS = False
    AWS_QUERYSTRING_AUTH = False
    AWS_PRELOAD_METADATA = True
    # URL prefix for static files.
    STATIC_URL = 'http://jailbreak14.s3.amazonaws.com/static/'

    # django compressor
    #COMPRESS_URL = STATIC_URL
    #COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    DEFAULT_PROFILER = STATIC_URL + 'base/images/jailbreak-profiler.jpg'


UPLOADS_URL = 'http://jailbreak14.s3.amazonaws.com/jailbreak14/'

# Localisation
TIME_ZONE = 'Europe/Dublin'
LANGUAGE_CODE = 'en-us'
DEFAULT_LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True

# Name of the directory that uploaded files should be put in.
UPLOADS_DIRNAME = 'uploads'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.normpath(os.path.join(DIRNAME, '..', UPLOADS_DIRNAME)) + os.path.sep

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/%s/' % UPLOADS_DIRNAME

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = os.path.normpath(os.path.join(DIRNAME, '..', 'static'))

# Additional locations of static files
STATICFILES_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = "b2052d6e-ab87-45fb-a80e-83790c54ad037cac7022-7fa9-4fdc-808d-2d8faff813d70545bb68-6506-45e3-9e07-0393591be717"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    'templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'utilities.context_processors.jailbreak_settings'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.flatpages',

    # 3rd party apps
    'south',
    'crispy_forms',
    #'compressor',
    'storages',

    # apps
    'accounts',
    'teams',
    'feeds',
    'utilities'
)

if not DEBUG:
    INSTALLED_APPS += (
        'gunicorn',
    )

def get_cache():
  import os
  try:
    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS']
    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ['MEMCACHIER_SERVERS'],
        'TIMEOUT': 500,
        'BINARY': True,
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()

# List of additional directories to look for fixtures in.
FIXTURE_DIRS = []
# Iterate all installed apps
for app_name in INSTALLED_APPS:
    # Determine the path to a 'fixtures_test' dir in the app.
    test_fixtures_dir = os.path.join(DIRNAME, app_name, 'fixtures_test')
    # If it exists, add it to the list of locations to look for fixtures in.
    if os.path.exists(test_fixtures_dir):
        FIXTURE_DIRS.append(test_fixtures_dir),

TECH_ADMIN_EMAIL = 'bakerke@tcd.ie'

SITE_ID = 1
INTERNAL_IPS = ('127.0.0.1',)

CRISPY_FAIL_SILENTLY = not DEBUG
CRISPY_TEMPLATE_PACK = 'foundation'

COMPRESS_ENABLED = True

# Jailbreak Specific Things
START_LNG = -6.3098048
START_LAT = 53.3418701
RADIUS_EARTH = 6373.0

MAIN_SPONSOR_PAGE = 'http://www.sponsor.ie/jailbreak-14-1/event/jailbreak14/'
START_TIME = datetime.datetime(2014, 02, 22, 9) # 9am Saturday 22/Feb/2104

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


if DEBUG:
    # Try to import local_settings.
    try:
        from local_settings import *
    except ImportError:
        pass
