#!/usr/bin/env bash

stdout=logs/chatik.log
stderr=logs/chatik_err.log

pkill daphne
pkill python
pkill celery

pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic -c --no-input

daphne daphne chatik.asgi:application -b 0.0.0.0 -p 8080 -v2 >> ${stdout} 2>> ${stderr} &
python3 manage.py runworker -v2 >> ${stdout} 2>> ${stderr} &
celery worker -A chatik --loglevel=debug --concurrency=4 &
