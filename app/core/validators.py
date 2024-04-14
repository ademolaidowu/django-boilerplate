"""
    This file contains validators used in the entire project
"""

import re
from django.core.exceptions import ValidationError


def validate_username(value) -> str:
    """
    Function to ensure username contains only alphanumeric characters
    or underscores. Returns the username or validation error.
    """
    if not re.match(r"^[A-Za-z0-9_]+$", value):
        raise ValidationError("Username can only contain alphanumeric characters or underscores.")

    return value


def validate_name(value) -> str:
    """
    Function to ensure name contains only alphabet characters.
    Returns the name or validation error.
    """
    if not re.match(r"^[A-Za-z]+$", value):
        raise ValidationError("Names can only contain letters")

    return value


def validate_password_format(value) -> str:
    """
    Function to ensure password contains only alphanumeric characters
    or selected special characters and to check if length of password is greater than 8 characters.
    Returns the password or validation error.
    """
    if not re.match(r"^[A-Za-z0-9@!]+$", value):
        raise ValidationError("Password can only contain alphanumeric characters or special characters like @, !")
    elif len(value) < 8:
        raise ValidationError("Password needs to be at least 8 characters.")

    return value


def is_amount(value) -> float:
    """
    Function to ensure that numeric value is greater than 0.00
    Returns value or validation error.
    """
    if value <= 0:
        raise ValidationError("Invalid amount")

    return value


def validate_zip_code(value):
    """
    Validator function to validate ZIP code contains only numbers.
    """
    if not re.match(r"^\d+$", value):
        raise ValidationError("ZIP code must contain only numbers.")

    return value
