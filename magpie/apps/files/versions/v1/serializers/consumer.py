from rest_framework import serializers

from magpie.apps.files.models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = (
            'name',
            'token',
            'created_at',
            'updated_at',
        )
