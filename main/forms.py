from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from main.models import User


class RegistrationForm(forms.ModelForm):
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                                      label='Повтор пароля')

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example@mail.ru'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }
        labels = {
            'password': 'Пароль',
        }

    def clean_repeat_password(self):
        pwd = self.cleaned_data['password']
        repeat_pwd = self.cleaned_data['repeat_password']
        if pwd != repeat_pwd:
            raise ValidationError('Пароли не совпали.')
        return repeat_pwd

    def clean_password(self):
        pwd = self.cleaned_data['password']
        password_validation.validate_password(pwd)
        return pwd

    def save(self, **kwargs):
        return User.objects.create_user(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
