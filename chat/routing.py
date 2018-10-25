from django.conf.urls import url

from chat import consumers

websocket_urlpatterns = [
    url(r'^chats/(?P<chat_id>\d+)/$', consumers.ChatConsumer),
]