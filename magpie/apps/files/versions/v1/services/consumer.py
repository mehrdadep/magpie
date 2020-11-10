from django.utils.translation import gettext as _
from rest_framework.pagination import LimitOffsetPagination

from magpie.apps.files.models import Consumer
from magpie.apps.files.versions.v1.serializers.consumer import (
    ConsumerSerializer,
)
from magpie.core import api_exceptions
from magpie.core.helper import Helper


class ConsumerService:
    @classmethod
    def get_all(cls, request):
        c = Consumer.objects.all()
        if 'name' in request.query_params:
            c = c.filter(
                name__icontains=request.query_params['name'],
            )
        paginator = LimitOffsetPagination()
        consumer = paginator.paginate_queryset(c, request)
        consumer = ConsumerSerializer(consumer, many=True)

        return consumer.data, paginator

    @classmethod
    def get_one(cls, name):
        try:
            c = Consumer.objects.get(
                name=name,
            )
        except Consumer.DoesNotExist:
            raise api_exceptions.NotFound404(
                _("Consumer does not exits")
            )
        consumer = ConsumerSerializer(c)

        return consumer.data

    @classmethod
    def create(cls):
        consumer = Consumer()
        consumer.save()
        consumer = ConsumerSerializer(consumer)
        return consumer.data

    @classmethod
    def update(cls, name):
        try:
            consumer = Consumer.objects.get(
                name=name,
            )
        except Consumer.DoesNotExist:
            raise api_exceptions.NotFound404(
                _("Consumer does not exits")
            )
        consumer.token = Helper.generate_token()
        consumer.save()
        consumer = ConsumerSerializer(consumer)

        return consumer.data

    @classmethod
    def revoke(cls, name):
        try:
            consumer = Consumer.objects.get(
                name=name,
            )
        except Consumer.DoesNotExist:
            raise api_exceptions.NotFound404(
                _("Token does not exits")
            )
        consumer.delete()
        return True
