from django.shortcuts import render
from django.views.generic import ListView

from chat.models import Chat


class ChatList(ListView):
    model = Chat