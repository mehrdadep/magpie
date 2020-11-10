from django.conf.urls import url

from file_server.apps.files.versions.v1.api import file
from file_server.apps.files.versions.v1.api import token

urls = [
    url(
        r'^(?:v1/)?tokens/(?P<username>[^/]+)(?:/)?$',
        token.TokenAPIView.as_view(),
        name='token'
    ),
    url(
        r'^(?:v1/)?files(?:/)?$',
        file.FilesAPIView.as_view(),
        name='files'
    ),
    url(
        r'^(?:v1/)?files/(?P<file_id>[^/]+)(?:/)?$',
        file.FileAPIView.as_view(),
        name='file'
    ),
]
