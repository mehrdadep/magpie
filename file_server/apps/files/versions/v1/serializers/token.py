from rest_framework import serializers

from file_server.apps.files.models import AuthToken


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = (
            'username',
            'token',
        )