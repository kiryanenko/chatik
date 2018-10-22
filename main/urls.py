from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^accounts/login/$',  LoginView.as_view()),
    url(r'^accounts/logout/$', LogoutView.as_view()),
]
