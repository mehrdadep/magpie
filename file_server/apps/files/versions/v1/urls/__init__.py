from django.conf.urls import url

from file_server.apps.files.versions.v1.api import api

urls = [
    url(
        r'^(?:v1/)?files/$',
        api.FilesAPIView.as_view(),
        name='files'
    ),
    url(
        r'^(?:v1/)?files/(?P<file_id>[^/]+)/$',
        api.FileAPIView.as_view(),
        name='file'
    ),
]
