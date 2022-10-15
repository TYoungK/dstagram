"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
import sys
import environ

sys.modules['django.utils.six.moves.urllib.parse'] = __import__('six.moves.urllib.parse', fromlist=['urlencode'])
sys.modules['django.utils.six.moves.urllib.request'] = __import__('six.moves.urllib.request', fromlist=['urlopen'])
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

env = environ.Env(DEBUG=(bool, False))

# reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

AUTH_USER_MODEL = 'accounts.User'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photo',
    'accounts',
    'disqus',
    'django.contrib.sites',
    'storages',
    'imagekit',
    'crispy_forms',
    'crispy_tailwind',
    'channels',
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.dstagram',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dstagram',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'db',
        'PORT': '3306',
    }
}

DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/





#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# media file (as a upload file)\
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'

DISQUS_WEBSITE_SHORTNAME = 'dstagram-tyk'
SITE_ID = 1

AWS_ACCESS_KEY_ID = env('S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('S3_SECRET_ACCESS_KEY')

# 헤로쿠 업로드용
# AWS_ACCESS_KEY_ID = os.environ['S3_ACCESS_KEY']
# AWS_SECRET_ACCESS_KEY = os.environ['S3_SECRET_KEY']

AWS_REGION = env('AWS_REGION')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=691,200'}
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static'

DEFAULT_FILE_STORAGE = 'config.asset_storage.MediaStorage'
#PROFILE_FILE_STORAGE = 'config.asset_storage.ProfileStorage'

STATIC_URL = 'http://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'config.asset_storage.StaticStorage'

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'django.request': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'django.request': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.request',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'gunicorn.log',
            'when': 'h',
            'formatter': 'verbose',
        },
        'django_logs': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'django.log',
            'when': 'h',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', ],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server', ],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['django.request'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.logs': {
            'level': 'DEBUG',
            'handlers': ['gunicorn'],
            'propagate': True,
        },
        'django.all_logs': {
            'level': 'DEBUG',
            'handlers': ['django_logs'],
            'propagate': False,
        },
    }
}
