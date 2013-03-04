import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# DEBUG = True
# TEMPLATE_DEBUG = DEBUG

CURRENT_CONFERENCE_ID = 1

SECRET_KEY = ''

DATABASES = {
    'development': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tcamp',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'production': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}
DATABASES['default'] = DATABASES['development']

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INTERNAL_IPS = ('127.0.0.1',)

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''
GOOGLE_OAUTH2_CLIENT_ID = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''
GITHUB_APP_ID = ''
GITHUB_API_SECRET = ''
DISQUS_CLIENT_ID = ''
DISQUS_CLIENT_SECRET = ''

DISQUS_SHORTNAME = ''
BRAINSTORM_USE_DISQUS = True
BRAINSTORM_LOGIN_OPTIONS = (
    ('Twitter', '/login/twitter/'),
    ('Facebook', '/login/facebook/'),
    ('Google', '/login/google-oauth2/'),
    ('Github', '/login/github/'),
)

POSTMARK_API_KEY = ''
POSTMARK_SENDER = ''

UNCON_FLICKR_API_KEY = ''
UNCON_FLICKR_TAGS = ''

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
COMPRESS_URL = '/static/'
COMPRESS_STORAGE = 'compressor.storage.CompressorFileStorage'
STATICFILES_STORAGE = COMPRESS_STORAGE
STATIC_URL = COMPRESS_URL
