from html import escape

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.dispatch import receiver

from chat.models import Chat


channel_layer = get_channel_layer()


class ChatConsumer(JsonWebsocketConsumer):
    GROUP_PREFIX = 'chat_'

    def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            self.close()
            return

        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        try:
            self.chat = Chat.objects.get(id=self.chat_id)
        except Chat.DoesNotExist:
            self.close()
            return

        if self.user not in self.chat.users:
            self.close()
            return

        self.room_group_name = self.chat_group_name(self.chat_id)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive_json(self, content, **kwargs):
        if content['type'] == 'has_read':
            self.has_read()

    def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def has_read(self):
        self.chat.user_has_read(self.user)

    def new_message(self, data):
        if self.user.email != data['data']['author']:
            self.send_json(data)

    def user_has_read(self, data):
        self.send_json(data)

    @classmethod
    def chat_group_name(cls, chat_id):
        return cls.GROUP_PREFIX + str(chat_id)

    @staticmethod
    @receiver(Chat.new_message)
    def group_send_new_message(sender, message, **kwargs):
        data = {
            'type': 'new_message',
            'data': message.to_dict
        }
        async_to_sync(channel_layer.group_send)(ChatConsumer.chat_group_name(sender.pk), data)

    @staticmethod
    @receiver(Chat.has_read)
    def group_send_user_has_read(sender, user, **kwargs):
        async_to_sync(channel_layer.group_send)(ChatConsumer.chat_group_name(sender.pk), {
            'id': sender.pk,
            'user': user.email,
            'type': 'user_has_read'
        })

