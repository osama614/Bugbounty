
from .base import *

#SECRET_KEY = env('SECRET_KEY')
SECRET_KEY= 'or!473&bx2l4lc5vx^k-3#2@kh@jrv5g485btq5i+m9otzk0w8'
DEBUG = True

ALLOWED_HOSTS = ['localhost',"127.0.0.1" ]


INSTALLED_APPS += [
    'debug_toolbar',
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ah.khaled2020@gmail.com'
EMAIL_HOST_PASSWORD = 'flgxozfsuexnljrj'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'ah.khaled2020@gmail.com'

# DEBUG_TOOLBAR_CONFIG = {
#     'JQUERY_URL': '',
# }

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


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "static"


STATICFILES_DIRS = [
   BASE_DIR / "static",
   '/var/www/static/',
]

STATIC_ROOT = "/var/www/example.com/static/"
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / "media"

# AWS_ACCESS_KEY_ID = 'AKIA5C6JEJFNUHDVAZV6'
# AWS_SECRET_ACCESS_KEY = 'WElIn17D/pJpT9QClJuOoVOhCGIMrCWHgQdNDO5a'

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