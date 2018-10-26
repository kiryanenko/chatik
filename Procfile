web: daphne chatik.asgi:application -b 0.0.0.0 -p $PORT -v2
worker: python manage.py runworker -v2
worker: celery worker -A chatik --loglevel=debug --concurrency=4