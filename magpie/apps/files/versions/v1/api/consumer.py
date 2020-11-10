from rest_framework import exceptions, status
from rest_framework.views import APIView

from magpie.apps.files.versions.v1.services.consumer import ConsumerService
from magpie.core.permissions import AdminAPIUserPermission
from magpie.core.response import response


class ConsumersAPIView(APIView):
    permission_classes = (AdminAPIUserPermission,)
    parser_classes = []

    def get(
            self,
            request,
            *args,
            **kwargs,
    ):
        try:
            r = ConsumerService.get_all(
                request,
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
            *args,
            **kwargs,
    ):
        try:
            r = ConsumerService.create()
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_201_CREATED,
            data=r,
        )


class ConsumerAPIView(APIView):
    permission_classes = (AdminAPIUserPermission,)
    parser_classes = []

    def get(
            self,
            request,
            name,
            *args,
            **kwargs,
    ):
        try:
            r = ConsumerService.get_one(name)
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_200_OK,
            data=r,
        )

    def patch(
            self,
            request,
            name,
            *args,
            **kwargs,
    ):
        try:
            r = ConsumerService.update(name)
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
            name,
            *args,
            **kwargs,
    ):
        try:
            ConsumerService.revoke(name)
        except exceptions.APIException as e:
            return response(request, error=e.detail, status=e.status_code)

        return response(
            request,
            status=status.HTTP_204_NO_CONTENT,
        )
