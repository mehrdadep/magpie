from django.conf import settings
from rest_framework import permissions

from magpie.apps.files.models import Consumer


class AdminAPIUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.META.get('HTTP_AUTHORIZATION'):
            auth_key = str(
                request.META.get('HTTP_AUTHORIZATION')
            ).lower()
            if 'bearer ' in auth_key:
                if settings.MAGPIE['ADMIN_API_KEY'] == auth_key.replace(
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
                    consumer = Consumer.objects.get(
                        token=token
                    )
                except Consumer.DoesNotExist:
                    return False

                request.consumer = consumer
                return True

        return False
