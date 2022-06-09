from django.contrib import admin
from .models import *
# Register your models here.


class PhotoInline(admin.TabularInline):
    model = Photo
    max_num = 10
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','author','created','updated']
    raw_id_fields = ['author']
    list_filter = ['created','updated','author']
    search_fields = ['text', 'created']
    ordering = ['-updated','-created']
    inlines = [PhotoInline, ]


class FollowAdmin(admin.ModelAdmin):
    list_display = ['id','user','follow','created']
    raw_id_fields = ['user','follow']
    list_filter = ['created','user','follow']
    search_fields = ['user', 'follow']
    ordering = ['-created']


class HeartAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created']
    raw_id_fields = ['post', 'user', 'post']
    list_filter = ['created', 'user', 'post']
    search_fields = ['user', 'post']
    ordering = ['-created']


admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, HeartAdmin)