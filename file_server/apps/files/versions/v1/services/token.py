from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.translation import gettext as _

from file_server.apps.files.models import AuthToken
from file_server.apps.files.versions.v1.serializers.token import (
    AuthTokenSerializer,
)
from file_server.core import api_exceptions
from file_server.core.helper import Helper


class TokenService:
    @classmethod
    def get(cls, username):
        try:
            token = AuthToken.objects.get(
                owner__username=username,
            )
        except User.DoesNotExist:
            raise api_exceptions.NotFound404(
                _("Token does not exits")
            )
        auth = AuthTokenSerializer(
            token
        )

        return auth.data

    @classmethod
    def create(cls, username):
        try:
            user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            raise api_exceptions.NotFound404(
                _("User does not exits")
            )
        token = AuthToken()
        token.owner = user
        try:
            token.save()
        except IntegrityError:
            raise api_exceptions.Conflict409(
                _("This user already has an auth token")
            )

        auth = AuthTokenSerializer(
            token
        )

        return auth.data

    @classmethod
    def update(cls, username):
        try:
            token = AuthToken.objects.get(
                owner__username=username,
            )
        except User.DoesNotExist:
            raise api_exceptions.NotFound404(
                _("Token does not exits")
            )
        token.token = Helper.generate_token()
        token.save()
        auth = AuthTokenSerializer(
            token
        )

        return auth.data

    @classmethod
    def revoke(cls, username):
        try:
            token = AuthToken.objects.get(
                owner__username=username,
            )
        except User.DoesNotExist:
            raise api_exceptions.NotFound404(
                _("Token does not exits")
            )
        token.delete()

        return True
