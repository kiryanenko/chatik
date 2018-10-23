from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from main.views import RegistrationView

urlpatterns = [
    url(r'^accounts/registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^accounts/login/$',  LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(), name='logout'),
]
