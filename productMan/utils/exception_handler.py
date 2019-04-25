# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _

from rest_framework.views import exception_handler
from rest_framework.exceptions import (Throttled, PermissionDenied,
                                       AuthenticationFailed)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):
        custom_response_data = {
            'detail':
                _('Request was throttled. '
                  'Expected available in {} seconds.').format(exc.wait)
        }
        response.data = custom_response_data

    if isinstance(exc, PermissionDenied):
        custom_response_data = {
            'detail': _('You do not have permission to perform this action.')
        }
        response.data = custom_response_data

    if isinstance(exc, AuthenticationFailed):
        custom_response_data = {
            'detail':
                _('Authentication credentials were not provided.')
        }
        response.data = custom_response_data

    return response
