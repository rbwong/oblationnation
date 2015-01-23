"""
Django settings for oblationnation project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from .base import * # import common settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h+7_66pqb-^n42wg#&dx0zj*&hgp-p5up0*nh16pw^mli7mfgo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += (
    'django_extensions',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oblationnation',
        'USER': 'root',
        'PASSWORD': '5233313.',
        'HOST': 'localhost',
    }
}

# Email service
# We will only use the console email backend for development and debugging
# purposes.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_URL = '/static/'

STATIC_ROOT = 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = 'media'
