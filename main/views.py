from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from main.forms import RegistrationForm
from main.models import User


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/registration.html'

    def get_success_url(self):
        return reverse('email_verification')


class EmailVerificationView(View):
    def get(self, request, uuid=None, *args, **kwargs):
        if uuid is None:
            return render(request, 'registration/email_verification.html')

        user = get_object_or_404(User, verification_uuid=uuid)
        user.verify()

        return render(request, 'registration/success_ email_verification.html')
