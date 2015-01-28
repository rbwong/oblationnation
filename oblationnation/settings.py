"""
Django common settings for DCS_Website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
STATIC_PATH = os.path.join(PROJECT_PATH,'static')

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static/media')
MEDIA_URL = '/static/media/'

# Handling missing secret keys
# From Two Scoops of Django
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable!!!" % var_name
        raise ImproperlyConfigured(error_msg)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h+7_66pqb-^n42wg#&dx0zj*&hgp-p5up0*nh16pw^mli7mfgo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oblation',
        'USER': 'upce',
        'PASSWORD': '123',
        'HOST': 'localhost',
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'django_extensions',
    'shop',
    'shop.addressmodel',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

PROJECT_APPS = (
    'order',
    'oblation',
)
INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'oblationnation.urls'

WSGI_APPLICATION = 'oblationnation.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = "/opt/oblationnation/static/"

MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
MEDIA_URL = '/static/media/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
)
# Django-Grappelli Settings

GRAPPELLI_ADMIN_TITLE="Oblation Nation"
GRAPPELLI_INDEX_DASHBOARD = {
    'django.contrib.admin.site': 'dashboard.CustomIndexDashboard'
}

# Django-FileBrowser Settings
FILEBROWSER_DIRECTORY='uploads/'
FILEBROWSER_VERSIONS_BASEDIR='_versions/'
FILEBROWSER_ADMIN_THUMBNAIL = 'admin_thumbnail'
FILEBROWSER_OVERWRITE_EXISTING = True

# Email service
# We will only use the console email backend for development and debugging
# purposes.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
