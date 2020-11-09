#!/bin/bash
pipenv run python manage.py compilemessages  && \
pipenv run python manage.py makemigrations && \
pipenv run python manage.py migrate && \
pipenv run python manage.py collectstatic --noinput  && \
pipenv run python manage.py createsuperuser && \
echo "File server installed successfully"
