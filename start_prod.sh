#!/bin/bash -e

python manage.py collectstatic --noinput --clear

python manage.py makemessages -l ru
python manage.py makemessages -l en
python manage.py compilemessages

python manage.py makemigrations --noinput
python manage.py migrate --noinput

gunicorn -b "0.0.0.0:8080" core.wsgi:application --workers $COMPOSE_WORKERS --timeout $COMPOSE_TIMEOUT