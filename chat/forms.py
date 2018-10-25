from django import forms
from django.core.exceptions import ValidationError

from chat.models import Chat
from main.models import User


class ChatForm(forms.Form):
    second_user = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Поиск по email'}), label='')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ChatForm, self).__init__(*args, **kwargs)

    def clean_second_user(self):
        second_user_email = self.cleaned_data['second_user']

        try:
            return User.objects.get_user_by_email(second_user_email)
        except User.DoesNotExist:
            raise ValidationError('Пользователь не найден.')

    def save(self):
        second_user = self.cleaned_data['second_user']
        return Chat.objects.get_or_create_chat(self.user, second_user)
