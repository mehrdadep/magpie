from django.conf.urls import url
from django.contrib import admin

from file_server.apps.files.versions.v1.api import api

urls = [
    url(r'^(?:v1/)?files/$', api.FilesAPIView.as_view()),
    url(r'^(?:v1/)?files/(?P<file_id>[0-9]+)/.*$', api.FileAPIView.as_view()),
]
