# Django settings for transparencycamp project.
import datetime
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jeremy Carbaugh', 'jcarbaugh@sunlightfoundation.com'),
    ('Dan Drinkard', 'ddrinkard@sunlightfoundation.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True

AWS_STORAGE_BUCKET_NAME = "assets.transparencycamp.org"
S3_URL = 'http://assets.transparencycamp.org.s3.amazonaws.com/2.0/'
COMPRESS_URL = S3_URL + 'static/'
COMPRESS_STORAGE = 's3utils.StaticRootS3BotoStorage'
STATICFILES_STORAGE = COMPRESS_STORAGE
STATIC_ROOT = '.static_cache'
STATIC_URL = COMPRESS_URL
ADMIN_MEDIA_PREFIX = '/static/admin/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "social_auth.context_processors.social_auth_by_type_backends",
    "social_auth.context_processors.social_auth_login_redirect",
    "brainstorm.context_processors.brainstorm",
)

AUTHENTICATION_BACKENDS = (
    'googleauth.backends.GoogleAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.disqus.DisqusBackend',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGOUT_URL = '/logout/'
GOOGLEAUTH_DOMAIN = 'sunlightfoundation.com'
GOOGLEAUTH_IS_STAFF = True
GOOGLEAUTH_REALM = 'transparencycamp.org'
SOCIAL_AUTH_UUID_LENGTH = 3
ROOT_URLCONF = 'transparencycamp.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'template_repl',
    'brainstorm',
    'markupwiki',
    'tastypie',
    'social_auth',
    'storages',
    'compressor',
    'transparencycamp.uncon',
    'gunicorn',
)

EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

CURRENT_CONFERENCE_ID = 1
MARKUPWIKI_EDITOR_TEST_FUNC = lambda u: True
MARKUPWIKI_AUTOLOCK_TIMEDELTA = datetime.timedelta(0, 60 * 60 * 23)

try:
    from local_settings import *
except ImportError:
    pass
