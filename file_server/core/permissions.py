from django.conf import settings
from rest_framework import permissions

from file_server.apps.files.models import AuthToken


class AdminAPIUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.META.get('HTTP_AUTHORIZATION'):
            auth_key = str(
                request.META.get('HTTP_AUTHORIZATION')
            ).lower()
            if 'bearer ' in auth_key:
                if settings.FILE_SERVER['ADMIN_API_KEY'] == auth_key.replace(
                        'bearer ',
                        '',
                ).strip():
                    return True

        return False


class FileAPIUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.META.get('HTTP_AUTHORIZATION'):
            auth_key = str(
                request.META.get('HTTP_AUTHORIZATION')
            ).lower()
            if 'bearer ' in auth_key:
                token = auth_key.replace('bearer ', '').strip()
                try:
                    api_key = AuthToken.objects.get(
                        token=token
                    )
                except AuthToken.DoesNotExist:
                    return False

                request.user = api_key.owner
                return True

        return False
