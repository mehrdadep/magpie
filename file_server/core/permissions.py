from rest_framework import permissions

from file_server.apps.files.models import UserToken


class UploadDownloadAPIUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_key = request.META.get('HTTP_AUTHORIZATION')

        user_token = UserToken.objects.filter(
                user_token=auth_key
        )
        if user_token.count() == 1:
            request.user = user_token[0].owner
            return True

        return False
