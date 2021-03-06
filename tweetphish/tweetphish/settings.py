"""
Django settings for tweetphish project.

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
SECRET_KEY = 'x*i=)c8e&5+$%d(a$o_f1jgt(0*7el(d_-vhvpetgpf50gq0nc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'endless_pagination',
    'tweets',
    'compressor',
    'south'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tweetphish.urls'

WSGI_APPLICATION = 'tweetphish.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "static"),
#)
#STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATIC_ROOT = ''
COMPRESS_ROOT = os.path.join(BASE_DIR, "static/")
COMPRESS_ENABLED = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join('static'),
)
# Twitter Oauth credentials
TWITTER_USER = "nilesh1013"
TWITTER_CACHE_TIMEOUT = 600
TWITTER_CONSUMER_KEY = "1qOjc1vYZkfofouQxp6h6A"
TWITTER_CONSUMER_SECRET = "RfmtPbHSBJvgC6dMTgxLmbDmR13KlMlDe5zLyNs"
TWITTER_OAUTH_TOKEN = "356735341-IJsaQyXjUih5nawaTMpz2FhqYtzHsdhsrRtbIKSn"
TWITTER_OAUTH_TOKEN_SECRET = "atrn6kUIwc31LqsUPmhrMCquYCIAKB6BAG9OVgzdCp549"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
TWITTER_TIMEOUT = 1200

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"tweetphish.custom_context.latest_tweet",
"django.core.context_processors.request")