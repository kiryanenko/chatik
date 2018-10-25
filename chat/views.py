from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from chat.forms import ChatForm
from chat.models import Chat


class UserChatsView(ListView):
    model = Chat

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form = ChatForm()

    def get_queryset(self):
        return Chat.objects.user_chats(self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.form = ChatForm(request.user, data=request.POST)
        if self.form.is_valid():
            chat = self.form.save()
            return HttpResponseRedirect(reverse('chat_detail', kwargs={'pk': chat.pk}))

        return self.get(request, *args, **kwargs)


class ChatDetail(DetailView):
    model = Chat
