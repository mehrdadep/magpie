from rest_framework import permissions

from file_server.apps.files.models import UserToken


class UploadDownloadAPIUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_key = request.META.get('HTTP_AUTHORIZATION')

        if UserToken.objects.filter(
                user_token=auth_key
        ).count() > 0:
            return True

        return False
