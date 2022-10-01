import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from accounts.models import User
from .models import Room, Message


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.opponent = None
        self.room_group_name = None
        self.room = None
        self.user = None

    def connect(self):
        try:
            self.opponent = self.scope['url_route']['kwargs']['opponent_tag']
            self.user = self.scope['user']
            room_exist = Room.objects.filter(users__tag=self.user.tag).filter(users__tag=self.opponent)
            self.room = room_exist[0] if room_exist.count() else Room.objects.create()
            self.room_group_name = f'chat_{self.room.id}'

            self.accept()

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name,
            )

            self.room.users.add(self.user)
            self.room.users.add(User.objects.get(tag=self.opponent))
            self.room.save()
            if room_exist.count():
                self.send(json.dumps({
                    'type': 'chat_catalog',
                    'messages': [{"user_profile": msg.user.profile_pic.url, "user_tag": msg.user.tag,
                                  "user_name": msg.user.name, "content": msg.content,
                                  "my_message": self.user == msg.user, "time": msg.timestamp}
                                 for msg in Message.objects.filter(room=self.room)],
                    'users': [user.name for user in self.room.users.all()],
                }, cls=DjangoJSONEncoder))
        except Exception as e:
            print(e)




    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        # if self.user.is_authenticated:
        #     self.room.users.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.tag,
                'message': message,
            }
        )
        Message.objects.create(user=self.user, room=self.room, content=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

