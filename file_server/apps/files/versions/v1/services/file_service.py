import os

from django.conf import settings
from django.utils.translation import gettext as _

from file_server.apps.files.models import File
from file_server.apps.files.versions.v1.serializers.serializers import (
    FileSerializer,
    FilesSerializer,
)
from file_server.core import api_exceptions


class FileService:
    @classmethod
    def upload_file(cls, request):
        file = request.FILES['file']
        # Check if file is greater than max upload size
        if float(file.size) > float(settings.FILE_SERVER['MAX_UPLOAD_SIZE']):
            raise api_exceptions.ValidationError400({
                'file_size': _('File is larger than expected'),
                'max_size': settings.FILE_SERVER['MAX_UPLOAD_SIZE'],
            })
        request.data['owner'] = request.user.id
        serializer = FileSerializer(
            data=request.data,
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return True

    @classmethod
    def download_file(cls, request, file_id):
        # Ensure that the file belongs to logged on user

        try:
            file_object = File.objects.get(
                file_id=file_id,
                owner=request.user,
            )
        except File.DoesNotExist:
            raise api_exceptions.NotFound404(
                _('File does not exists or does not belongs to this user'),
            )
        path = file_object.file.path

        return (
            os.path.basename(path),
            os.path.dirname(path),
        )

    @classmethod
    def get_files(cls, request):
        files = File.objects.filter(
            owner=request.user,
        )
        files_serializer = FilesSerializer(
            files,
            many=True
        )

        return files_serializer.data

    @classmethod
    def generate_user_token(
            cls,
            user_id,
    ):
        pass
