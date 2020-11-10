from rest_framework import permissions

from file_server.apps.files.models import ApiKey


class UploadDownloadAPIUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.META.get('HTTP_AUTHORIZATION'):
            auth_keys = request.META.get('HTTP_AUTHORIZATION').split(',')
            for auth_key in auth_keys:
                if 'ApiKey-Files' in auth_key:
                    api_key_file = auth_key.replace('ApiKey-Files ', '').strip()
                    api_key = ApiKey.objects.filter(
                            api_key=api_key_file
                    )
                    if api_key.count() == 1:
                        request.user = api_key[0].owner
                        return True

        return False
