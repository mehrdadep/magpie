import os
import uuid
from datetime import datetime

from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.pagination import LimitOffsetPagination

from magpie.apps.files.models import File
from magpie.apps.files.versions.v1.serializers.file import (
    FileSerializer,
    FilesSerializer,
)
from magpie.core import api_exceptions
from magpie.core.cache import Cache


class FileService:
    @classmethod
    def upload_file(cls, request):
        file_keys = dict(request.FILES).keys()
        uploaded_files = []
        for file_key in file_keys:
            file_data = {}
            file = request.FILES[file_key]
            file_data['file'] = request.data[file_key]
            file_data['consumer'] = request.consumer.id
            file_data['file_name'] = request.FILES[file_key].name

            # Check if file is greater than max upload size
            if float(file.size) > float(
                    settings.MAGPIE['MAX_UPLOAD_SIZE']):
                raise api_exceptions.ValidationError400({
                    'file_size': _('File is larger than expected'),
                    'max_size': f"{settings.MAGPIE['MAX_UPLOAD_SIZE']} "
                                f"bytes",
                })

            file_serializer = FileSerializer(
                data=file_data,
            )

            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()
                uploaded_files.append(
                    file_serializer.data
                )

        upload_message = _("Count of uploaded files")
        done_files_count = len(uploaded_files)
        return {
            "message": f"{upload_message}: {done_files_count}",
            "count": done_files_count,
            "files": uploaded_files,
        }

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
                    consumer=request.consumer,
                )
                Cache.set(
                    key=str(f"file_id:{file_id}-user_id:{request.user.id}"),
                    store_value=file_object,
                    expiry_time=settings.MAGPIE['CACHE_EXPIRY'],
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
        files_query = File.objects.filter(
            consumer=request.consumer,
        )

        if request.query_params is not None:
            if 'created_at_from' in request.query_params:
                try:
                    created_at_from = datetime.fromtimestamp(
                        float(request.query_params['created_at_from'])
                    )
                    files_query = files_query.filter(
                        created_at__gte=created_at_from
                    )
                except ValueError:
                    raise api_exceptions.ValidationError400(
                        detail={
                            'created_at_from': _("Datetime parsing error")
                        }
                    )

            if 'created_at_to' in request.query_params:
                try:
                    created_at_to = datetime.fromtimestamp(
                        float(request.query_params['created_at_to'])
                    )
                    files_query = files_query.filter(
                        created_at__lte=created_at_to
                    )
                except ValueError:
                    raise api_exceptions.ValidationError400(
                        detail={
                            'created_at_to': _("Datetime parsing error")
                        }
                    )

            # Order by
            if 'order_by' in request.query_params:
                order_field_error = []
                order_by = [
                    x.strip() for x in request.query_params
                    ['order_by'].split(',')
                ]
                for order in order_by:
                    if not File.model_field_exists(
                            order.replace('-', ''),
                    ):
                        order_field_error.append(order)
                if order_field_error:
                    raise api_exceptions.ValidationError400(
                        {
                            'non_fields': _("Invalid choices in order by "
                                            "query"),
                            'errors': order_field_error,
                        }
                    )

                files_query = files_query.order_by(
                    *order_by
                )

        paginator = LimitOffsetPagination()
        files_query = paginator.paginate_queryset(files_query, request)
        files_serializer = FilesSerializer(
            files_query,
            many=True
        )

        return files_serializer.data, paginator

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
                consumer=request.consumer,
            )
        except File.DoesNotExist:
            raise api_exceptions.NotFound404(
                _('File does not exists or does not belongs to this consumer'),
            )

        Cache.delete(
            key=str(f"file_id:{file_id}-user_id:{request.user.id}"),
        )

        file_object.file.delete()
        file_object.delete()

        return True
