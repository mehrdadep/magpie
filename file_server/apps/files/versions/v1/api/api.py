from django.views.static import serve
from rest_framework import exceptions, status
from rest_framework.parsers import (
    MultiPartParser,
)
from rest_framework.views import APIView

from file_server.apps.files.versions.v1.services.file_service import (
    FileService,
)
from file_server.core.permissions import UploadDownloadAPIUserPermission
from file_server.core.response import response


class FilesAPIView(APIView):
    permission_classes = (UploadDownloadAPIUserPermission,)
    parser_classes = (MultiPartParser,)

    def post(
            self,
            request,
            *args,
            **kwargs,
    ):
        try:
            response_data = FileService.upload_file(
                request,
            )
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_201_CREATED,
            data=response_data,
        )

    def get(
            self,
            request,
            *args,
            **kwargs,
    ):
        try:
            response_data = FileService.get_files(
                request,
            )
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_201_CREATED,
            data=response_data,
        )


class FileAPIView(APIView):
    permission_classes = (UploadDownloadAPIUserPermission,)
    parser_classes = (MultiPartParser,)

    def get(
            self,
            request,
            file_id,
            *args,
            **kwargs,
    ):
        try:
            response_data = FileService.download_file(
                request,
                file_id,
            )
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return serve(
            request,
            response_data[0],
            response_data[1],
        )

    def delete(
            self,
            request,
            file_id,
            *args,
            **kwargs,
    ):
        try:
            FileService.delete_file(
                request,
                file_id,
            )
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_204_NO_CONTENT,
        )
