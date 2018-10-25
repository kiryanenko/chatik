from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView

from chat.forms import ChatForm, MessageForm
from chat.models import Chat, Message
from main.views import HttpResponseAjax, HttpResponseAjaxError


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


class ChatDetailView(DetailView):
    model = Chat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm()
        context['messages'] = self.object.messages.order_by('id')
        return context


@require_POST
@login_required
def create_message(request, chat_id=None):
    chat = get_object_or_404(Chat, id=chat_id)
    form = MessageForm(user=request.user, chat=chat, data=request.POST)
    if form.is_valid():
        msg = form.save()
        return HttpResponseAjax(message=msg.message, created_at=msg.created_at, user=msg.author)
    else:
        return HttpResponseAjaxError(errors=form.errors)
