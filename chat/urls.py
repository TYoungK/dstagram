from django.urls import path

from .views import *

app_name = "chat"

urlpatterns = [
    path('', index_view, name='chat-list'),
    path('<str:opponent_tag>/', room_view, name='chat-room'),
]