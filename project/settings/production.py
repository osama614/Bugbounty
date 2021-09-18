
from .base import *
import os


DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ["hackingt-dev.herokuapp.com"]

MIDDLEWARE.insert(2, 'whitenoise.middleware.WhiteNoiseMiddleware') 


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dev_bug_data',
        'USER': 'root',
        'PASSWORD': 'robot9000',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        #'PORT': '3306',
    }
}


import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
#DATABASES['default'] = dj_database_url.config(default='postgres://...'}
DATABASES['default'].update(db_from_env)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.titan.email'
EMAIL_HOST_USER = 'info@hackingt.com'
EMAIL_HOST_PASSWORD = 'vpeIqFMK7b'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@hackingt.com'


CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
  #  os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# AWS_ACCESS_KEY_ID = 'AKIA5C6JEJFNUHDVAZV6'
# AWS_SECRET_ACCESS_KEY = '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'

# AWS_STORAGE_BUCKET_NAME = 'bugbounty'
# #AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_CUSTOM_DOMAIN = 'd26fiq2525qngt.cloudfront.net'

# AWS_LOCATION = 'static'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

# STATICFILES_DIRS = [
#     BASE_DIR /'static',
# ]

# DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'