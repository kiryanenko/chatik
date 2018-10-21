from django.conf.urls import url

from chat.views import ChatList

urlpatterns = [
    url(r'^chats/$', ChatList.as_view(), name='chat_list'),
    url(r'^$', ChatList.as_view()),
]