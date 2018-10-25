from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from chat.views import UserChatsView, ChatDetailView, create_message

urlpatterns = [
    url(r'^chats/$', login_required(UserChatsView.as_view()), name='user_chats'),
    url(r'^chats/(?P<pk>\d+)/$', login_required(ChatDetailView.as_view()), name='chat_detail'),
    url(r'^chats/(?P<chat_id>\d+)/messages/$', create_message, name='create_message'),
    url(r'^$', login_required(UserChatsView.as_view())),
]