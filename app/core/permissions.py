"""
This file contains custom permission classes used throughout the project
"""

from rest_framework.permissions import BasePermission


class IsFullyGrantedPermission(BasePermission):
    """
    Custom permission to only allow access to authenticated users that profiles that are confirmed.
    """

    message = "User Profile registration is not complete"

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.profile.is_confirmed:
                return True
            return False

        return False
