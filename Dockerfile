FROM python:3.9-slim-buster
WORKDIR /file-server
RUN apt update && \
apt upgrade -y && \
apt install build-essential gettext -y && \
pip install pipenv && \
rm -rf /var/lib/apt/lists/*
COPY ./Pipfile /file-server
RUN pipenv update
COPY . /file-server
EXPOSE 8000
ENTRYPOINT ["pipenv", "run", "uwsgi", "--ini", "./docker/configs/uwsgi/uwsgi.ini"]
