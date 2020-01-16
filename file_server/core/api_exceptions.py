"""
Doc.
"""
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import (
    APIException as BaseAPIException,
    ValidationError as BaseValidationError,
)


def raise_exception(status_code, detail=None):
    """

    :param status_code:
    :param detail:
    :return:
    """
    exceptions = {
        status.HTTP_400_BAD_REQUEST: ValidationError400,
        status.HTTP_401_UNAUTHORIZED: NotAuthenticated401,
        status.HTTP_403_FORBIDDEN: PermissionDenied403,
        status.HTTP_404_NOT_FOUND: NotFound404,
        status.HTTP_409_CONFLICT: Conflict409,
        status.HTTP_410_GONE: Gone410,
        status.HTTP_500_INTERNAL_SERVER_ERROR: APIException,
    }

    if status_code in exceptions:
        exception_class = exceptions.get(status_code)

        raise exception_class(detail=detail)


class APIException(BaseAPIException):
    """
    Doc.
    """

    def __init__(self, detail=None, code=None, hint=None, **kwargs):
        super().__init__(detail, code)
        self.hint = hint


class ValidationError400(BaseValidationError):
    """
    Doc.
    """

    def __init__(self, detail=None, code=None, hint=None, **kwargs):
        super().__init__(detail, code)
        self.hint = hint


class AuthenticationFailed401(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Incorrect authentication credentials.')
    default_code = 'authentication_failed'


class NotAuthenticated401(APIException):
    """
    Doc.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided.')
    default_code = 'not_authenticated'


class PermissionDenied403(APIException):
    """
    Doc.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You do not have permission to perform this action.')
    default_code = 'permission_denied'


class NotFound404(APIException):
    """
    Doc.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('The requested resource could not be found.')
    default_code = 'not_found'


class Conflict409(APIException):
    """
    Doc.
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('The request could not be completed.')
    default_code = 'conflict'


class Gone410(APIException):
    """
    Doc.
    """
    status_code = status.HTTP_410_GONE
    default_detail = _('The requested resource is no longer available.')
    default_code = 'gone'


class TimeOut408(APIException):
    """
    Doc.
    """
    status_code = status.HTTP_408_REQUEST_TIMEOUT
    default_detail = _('Request timeout')
    default_code = 'timeout'
