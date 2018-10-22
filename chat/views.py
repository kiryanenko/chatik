from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from chat.models import Chat


@method_decorator(name='get', decorator=login_required)
class ChatList(ListView):
    model = Chat


class ChatDetail(DetailView):
    model = Chat
