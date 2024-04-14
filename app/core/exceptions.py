"""
This file contains custom exception handlers for format of responses of APIs in this project
"""

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Function to assign custom exception handlers based on exception class
    """

    handlers = {
        "ValidationError": _handle_generic_error,
        "Http404": _handle_generic_error,
        "PermissionDenied": _handle_generic_error,
        "NotAuthenticated": _handle_authentication_error,
    }

    response = exception_handler(exc, context)

    if response is not None:
        print(response.data)
        response.data["status_code"] = response.status_code

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_authentication_error(exc, context, response):
    response.data = {
        "message": "Please log in to proceed",
        "error": "Unauthorized User",
        "status_code": response.status_code,
    }
    return response


def _handle_generic_error(exc, context, response):
    return response
