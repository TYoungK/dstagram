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
def room_view(request, opponent_tag):
    # participant = User.objects.filter(tag__in=[request.user.tag, opponent_tag])
    room = Room.objects.filter(users__tag=request.user.tag).filter(users__tag=opponent_tag)
    if room.count() == 0:
        room = Room.objects.create()

    return render(request, 'room.html', {
        'room': room,
        'opponent': User.objects.get(tag=opponent_tag)
    })
