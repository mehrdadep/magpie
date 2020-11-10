from rest_framework import exceptions, status
from rest_framework.views import APIView

from file_server.apps.files.versions.v1.services.token import TokenService
from file_server.core.permissions import AdminAPIUserPermission
from file_server.core.response import response


class TokenAPIView(APIView):
    permission_classes = (AdminAPIUserPermission,)
    parser_classes = []

    def get(
            self,
            request,
            username,
            *args,
            **kwargs,
    ):
        try:
            r = TokenService.get(
                username,
            )
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_200_OK,
            data=r,
        )

    def post(
            self,
            request,
            username,
            *args,
            **kwargs,
    ):
        try:
            r = TokenService.create(
                username,
            )
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_201_CREATED,
            data=r,
        )

    def patch(
            self,
            request,
            username,
            *args,
            **kwargs,
    ):
        try:
            r = TokenService.update(
                username,
            )
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_200_OK,
            data=r,
        )

    def delete(
            self,
            request,
            username,
            *args,
            **kwargs,
    ):
        try:
            TokenService.revoke(
                username,
            )
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_204_NO_CONTENT,
        )
