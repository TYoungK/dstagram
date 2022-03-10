from django.contrib import admin
from .models import *
# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id','author','created','updated']
    raw_id_fields = ['author']
    list_filter = ['created','updated','author']
    search_fields = ['text', 'created']
    ordering = ['-updated','-created']

class FollowAdmin(admin.ModelAdmin):
    list_display = ['id','user','follow','created']
    raw_id_fields = ['user','follow']
    list_filter = ['created','user','follow']
    search_fields = ['user', 'follow']
    ordering = ['-created']

class HeartAdmin(admin.ModelAdmin):
    list_display = ['photo', 'user', 'created']
    raw_id_fields = ['photo', 'user', 'photo']
    list_filter = ['created', 'user', 'photo']
    search_fields = ['user', 'photo']
    ordering = ['-created']

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, HeartAdmin)