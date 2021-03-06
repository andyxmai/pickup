"""
Django settings for pickup project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@i^jn^q3%#uwngsj%42ns@42bw3mxpv4*xap1%j+7=4w!ik1dg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG = not os.environ.get('REQTIME_PRODUCTION', False)

ADMINS = (
    ('Andy Mai', 'andrew.x.mai@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {}

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

if DEBUG:
    FACEBOOK_APP_ID              = '703715933005935'
    FACEBOOK_API_SECRET          = 'db08833ea92e2d493fe0b17d74b4cf42'
    FACEBOOK_URL                 = 'http://127.0.0.1:8000/profile/'

    INSTAGRAM_ID = '91352210f6374c08a9b3c20286c6d8e7'
    INSTAGRAM_SECRET = 'd8b74583559c491cb7373f8733cc95ec'
    REDIRECT_URL = 'http://127.0.0.1:8000/instagram_login'
else:
    FACEBOOK_APP_ID              = '386574128151198'
    FACEBOOK_API_SECRET          = '6223003370aaebb550559494027c111d'
    FACEBOOK_URL                 = 'http://reqtime.herokuapp.com/profile/'

    INSTAGRAM_ID = '845a7a26a2b843cd960fca5f87c50d56'
    INSTAGRAM_SECRET = '007324e2cf8b464886cb51dd57717ccd'
    REDIRECT_URL = 'http://reqtime.herokuapp.com/instagram_login'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pickupApp',
    'notifications',
    'actstream',
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

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.disqus.DisqusBackend',
    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    'social_auth.backends.contrib.orkut.OrkutBackend',
    'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.vk.VKOAuth2Backend',
    'social_auth.backends.contrib.live.LiveBackend',
    'social_auth.backends.contrib.skyrock.SkyrockBackend',
    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    'social_auth.backends.contrib.readability.ReadabilityBackend',
    'social_auth.backends.contrib.fedora.FedoraBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

ACTSTREAM_SETTINGS = {
    'MODELS': ('pickupApp.Game', 'pickupApp.GamePhoto','pickupApp.UserInfo','auth.user', 'auth.group', 'sites.site', 'comments.comment'),
    #'MANAGER': 'myapp.streams.MyActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}


ROOT_URLCONF = 'pickup.urls'

WSGI_APPLICATION = 'pickup.wsgi.application'


if DEBUG:
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL           = '/'
LOGIN_REDIRECT_URL  = '/home/'
LOGIN_ERROR_URL     = '/'


# Email Settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'debugsafedriven@gmail.com'
EMAIL_HOST_PASSWORD = 'fratpad2014'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Static asset configuration
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'pickupApp/static'),
)

