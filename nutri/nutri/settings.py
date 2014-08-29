"""
Django settings for nutri project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i!4^1(9w)3c6m0wbd_d(8e0zpkk#d)5idx2j#ozdwhkb)e(i6s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    '/Users/campbellweaver/Documents/Personal/NutriApp/NutriApp/nutri/templates',
)

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'bootstrap').replace('\\','/'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ingred_table',
    'autocomplete_light',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nutri.urls'

WSGI_APPLICATION = 'nutri.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#   'HOST': 'ec2-54-200-21-53.us-west-2.compute.amazonaws.com',

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'ingredients',
    'HOST': 'ccweaverdbinstance.cjqflsribv1h.us-west-2.rds.amazonaws.com',
    'PORT': 5432,
    'USER': 'ccweaver',
    'PASSWORD': '1234567890'
  }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
