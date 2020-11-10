from django.conf.urls import url

from magpie.apps.files.versions.v1.api import file
from magpie.apps.files.versions.v1.api import consumer

urls = [
    url(
        r'^(?:v1/)?consumers(?:/)?$',
        consumer.ConsumersAPIView.as_view(),
        name='consumers'
    ),
    url(
        r'^(?:v1/)?consumers/(?P<name>[^/]+)(?:/)?$',
        consumer.ConsumerAPIView.as_view(),
        name='consumer'
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
