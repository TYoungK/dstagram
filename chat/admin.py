from django.contrib import admin
from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_users']
    search_fields = ['users__email']

    def get_users(self, obj):
        return obj.users.all()


class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'content', 'timestamp']
    list_filter = ['user', 'room']
    search_fields = ['user', 'room', 'content']



admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
