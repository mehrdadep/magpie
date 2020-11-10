from collections import OrderedDict

from django.utils import timezone
from rest_framework.response import Response as DRFResponse


class Response(DRFResponse):
    def __init__(
            self,
            request,
            data=None,
            redirect_to=None,
            status=200,
            error=None,
            hint=None,
            message=None,
            pagination=True,
    ):
        custom_response = OrderedDict()

        if data and request.method == 'GET' and status == 200 and not \
                isinstance(
                    data, dict) and pagination:
            data, paginator = data

            if paginator:
                custom_response.update([
                    ('count', paginator.count),
                    ('next', paginator.get_next_link()),
                    ('previous', paginator.get_previous_link()),
                ])

        # Check Type of 'error'.
        if isinstance(error, Exception):
            error = error.__str__()

        custom_response.update([
            ("status", status),
            ("error", error),
            ("hint", hint),
            ("message", message),
            ("user_id", request.user.id),
            ("time", timezone.now().strftime("%y%m%d%H%M%S")),
            ("data", data),
        ])

        if redirect_to:
            custom_response.update([
                ('redirect_to', redirect_to),
            ])

        super(Response, self).__init__(data=custom_response, status=status)


def response(
        request,
        status=200,
        data=None,
        error=None,
        hint=None,
        message=None,
        redirect_to=None,
        pagination=True,
):
    return Response(
        request=request,
        status=status,
        data=data,
        error=error,
        hint=hint,
        message=message,
        redirect_to=redirect_to,
        pagination=pagination,
    )
