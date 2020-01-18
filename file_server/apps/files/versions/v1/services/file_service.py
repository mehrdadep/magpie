import os
import uuid

from django.conf import settings
from django.utils.translation import gettext as _

from file_server.apps.files.models import File
from file_server.apps.files.versions.v1.serializers.serializers import (
    FileSerializer,
    FilesSerializer,
)
from file_server.core import api_exceptions
from file_server.core.cache import Cache


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
        try:
            if not isinstance(file_id, uuid.UUID):
                file_id = uuid.UUID(file_id)
        except ValueError:
            raise api_exceptions.ValidationError400(
                {
                    'id': _('Not a valid UUID')
                }
            )
        file_object = Cache.get(
            str(f"file_id:{file_id}-user_id:{request.user.id}"),
        )

        if not file_object:
            try:
                file_object = File.objects.get(
                    file_id=file_id,
                    owner=request.user,
                )
                Cache.set(
                    key=str(f"file_id:{file_id}-user_id:{request.user.id}"),
                    store_value=file_object,
                    expiry_time=settings.FILE_SERVER['CACHE_EXPIRY'],
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
    def delete_file(cls, request, file_id):
        try:
            if not isinstance(file_id, uuid.UUID):
                file_id = uuid.UUID(file_id)
        except ValueError:
            raise api_exceptions.ValidationError400(
                {
                    'id': _('Not a valid UUID')
                }
            )

        try:
            file_object = File.objects.get(
                file_id=file_id,
                owner=request.user,
            )
        except File.DoesNotExist:
            raise api_exceptions.NotFound404(
                _('File does not exists or does not belongs to this user'),
            )

        Cache.delete(
            key=str(f"file_id:{file_id}-user_id:{request.user.id}"),
        )

        file_object.file.delete()
        file_object.delete()

        return True
