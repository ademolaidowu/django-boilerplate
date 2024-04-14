"""
This file contains wrappers used throughout the project
"""


def use_default_response(view_func):
    """
    Function wrapper to rollback `BaseAPIResponseMiddleware`
    into default response middleware. Apply as decorator on view function as such -
    @method_decorator(use_default_response)
    """

    def wrapper_function(request, *args, **kwargs):
        request.META["HTTP_USE_DEFAULT_RESPONSE"] = True
        return view_func(request, *args, **kwargs)

    return wrapper_function
