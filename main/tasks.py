import logging

from django.core.mail import send_mail
from django.urls import reverse

from chatik.celery import app
from chatik.settings import CHATIK_HOST
from main.models import User


@app.task
def send_verification_email(user_id):
    try:
        user = User.objects.get(pk=user_id)
        send_mail(
            'Подтверждение email',
            'Для подтверждения вашего email перейдите по следующей ссылке: '
            '{}{}'.format(CHATIK_HOST, reverse('email_verification', kwargs={'uuid': str(user.verification_uuid)})),
            'from@chatik.ru',
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
