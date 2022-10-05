from .base import *

DEBUG = False

SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_CLOUDFRONT_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
LOGIN_REDIRECT_URL = '/'
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': env('DATABASE_NAME'),
#         'USER': env('DATABASE_USER'),
#         'PASSWORD': env('DATABASE_PASSWORD'),
#         'HOST': env('DATABASE_HOST'),
#         'PORT': env('DATABASE_PORT'),
#     }
# }
