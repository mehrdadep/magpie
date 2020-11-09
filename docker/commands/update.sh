#!/bin/bash
pipenv run python manage.py compilemessages && \
pipenv run python manage.py makemigrations && \
pipenv run python manage.py migrate && \
echo "File server updated successfully"
