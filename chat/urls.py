from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from chat.views import UserChatsView, ChatDetail

urlpatterns = [
    url(r'^chats/$', login_required(UserChatsView.as_view()), name='user_chats'),
    url(r'^chats/(?P<pk>\d+)/$', login_required(ChatDetail.as_view()), name='chat_detail'),
    url(r'^$', login_required(UserChatsView.as_view())),
]