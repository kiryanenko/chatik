from django.urls import reverse
from django.views.generic import CreateView

from main.forms import RegistrationForm
from main.models import User


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/registration.html'

    def get_success_url(self):
        return reverse('login')
