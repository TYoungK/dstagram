from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth.models import User

@shared_task
def get_users(user_name):
    return User.objects.filter(first_name__startswith=user_name)
