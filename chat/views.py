from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
from accounts.models import User


@login_required
def index_view(request):
    return render(request, 'index.html', {
        'rooms': request.user.room_set.all(),
    })


@login_required
def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })