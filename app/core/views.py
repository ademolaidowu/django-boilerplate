"""
This file contains global views for the project
"""

from django.http import JsonResponse


def error_404(request, exception):
    message = "The endpoint is not found"

    response = JsonResponse(data={"message": message, "error": "Not Found", "status_code": 404})
    response.status_code = 404

    return response


def error_500(request):
    message = "An error ocurred, we are working on it"

    response = JsonResponse(data={"message": message, "error": "Server Error", "status_code": 500})
    response.status_code = 500

    return response
