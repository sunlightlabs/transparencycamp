import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# DEBUG = True
# TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'development': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
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

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INTERNAL_IPS = ('127.0.0.1',)

POSTMARK_API_KEY = ''
POSTMARK_SENDER = ''

UNCON_FLICKR_API_KEY = ''
UNCON_FLICKR_TAGS = ''

MEDIASYNC = {
    'BACKEND': 'mediasync.backends.s3',
    'AWS_KEY': '',
    'AWS_SECRET': '',
    'AWS_BUCKET': '',
    'PROCESSORS': (
        'mediasync.processors.slim.css_minifier',
        'mediasync.processors.closurecompiler.compile',
    ),
}