"""Settings for testing django_newsletter"""

SITE_ID = 1

USE_I18N = False

SECRET_KEY = "testkey"

ROOT_URLCONF = 'django_newsletter.urls'

DATABASES = {'default': {'NAME': 'newsletter_tests.db',
                         'ENGINE': 'django.db.backends.sqlite3'}}

INSTALLED_APPS = ['django.contrib.contenttypes',
                  'django.contrib.sites',
                  'django.contrib.auth',
                  'tagging',
                  'django_newsletter']
