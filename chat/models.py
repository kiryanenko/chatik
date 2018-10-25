from django.db import models

from main.models import User


class ChatManager(models.Manager):
    def get_or_create_chat(self, first_user, second_user):
        try:
            return self.get(models.Q(first_user=first_user, second_user=second_user),
                            models.Q(first_user=second_user, second_user=first_user),)
        except Chat.DoesNotExist:
            return self.create(first_user=first_user, second_user=second_user)

    def user_chats(self, user):
        return self.filter(models.Q(first_user=user), models.Q(second_user=user))


class Chat(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    last_message = models.ForeignKey('Message', on_delete=models.CASCADE, null=True, related_name='+')

    objects = ChatManager()

    def companion(self, current_user):
        return self.second_user if current_user == self.first_user else self.first_user

    class Meta:
        unique_together = ('first_user', 'second_user')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
