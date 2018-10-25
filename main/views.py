import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from main.forms import RegistrationForm
from main.models import User


class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(content=json.dumps(kwargs), content_type='application/json')


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, errors):
        errors_dict = json.dumps(dict([(key, [err for err in value]) for key, value in errors.items()]))
        super(HttpResponseAjaxError, self).__init__(status='error', errors=errors_dict)


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
