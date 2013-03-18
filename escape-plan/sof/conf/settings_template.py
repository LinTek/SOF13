from sof.conf.settings_global import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sof13',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Set this to something interesting and random, and don't share it with anybody.
SECRET_KEY = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG


DEFAULT_FROM_EMAIL = 'SOF Funktionärsansvarig <mailer@sof13.se>'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
