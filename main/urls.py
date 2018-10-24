from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from main.views import RegistrationView, EmailVerificationView

urlpatterns = [
    url(r'^accounts/registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^accounts/email_verification/?(?P<uuid>[a-z0-9\-]+)?/$',
        EmailVerificationView.as_view(), name='email_verification'),
    url(r'^accounts/login/$',  LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(), name='logout'),
]
