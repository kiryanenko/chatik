from html import escape

from django.core.exceptions import PermissionDenied
from django.db import models
from django.dispatch import Signal

from main.models import User


class ChatManager(models.Manager):
    def get_or_create_chat(self, first_user, second_user):
        try:
            return self.get(models.Q(first_user=first_user, second_user=second_user) |
                            models.Q(first_user=second_user, second_user=first_user),)
        except Chat.DoesNotExist:
            return self.create(first_user=first_user, second_user=second_user)

    def user_chats(self, user):
        return self.filter(models.Q(first_user=user) | models.Q(second_user=user),
                           last_message__isnull=False).order_by('-last_message_id')


class Chat(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    last_message = models.ForeignKey('Message', on_delete=models.CASCADE, null=True, related_name='+')

    objects = ChatManager()

    new_message = Signal(providing_args=('message',))
    has_read = Signal(providing_args=('user',))

    def companion(self, current_user):
        return self.second_user if current_user == self.first_user else self.first_user

    def send_massage(self, user, msg):
        if user not in self.users:
            raise PermissionDenied()

        new_msg = Message.objects.create(author=user, chat=self, message=msg)
        self.last_message = new_msg
        self.save()

        self.new_message.send(self, message=new_msg)

        return new_msg

    def user_has_read(self, user):
        if user not in self.users:
            raise PermissionDenied()

        self.messages.exclude(author=user).update(has_read=True)
        self.has_read.send(self, user=user)

    @property
    def users(self):
        return {self.first_user, self.second_user}

    class Meta:
        unique_together = ('first_user', 'second_user')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    has_read = models.BooleanField(default=False, help_text='Было ли прочитано данное сообщение.')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def to_dict(self):
        return {
            'id': self.pk,
            'chat': self.chat.pk,
            'message': escape(self.message),
            'author': self.author.email,
            'has_read': self.has_read,
            'created_at': self.created_at.strftime("%b. %d, %Y, %H:%M"),
        }
