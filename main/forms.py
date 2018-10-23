from django import forms
from django.contrib.auth import password_validation

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

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        pwd = cleaned_data.get('password')
        repeat_pwd = cleaned_data.get('repeat_password')

        if pwd and repeat_pwd:
            if pwd != repeat_pwd:
                self.add_error('repeat_password', 'Пароли не совпали.')

        return cleaned_data

    def clean_password(self):
        pwd = self.cleaned_data['password']
        password_validation.validate_password(pwd)
        return pwd

    def save(self, **kwargs):
        return User.objects.create_user(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
