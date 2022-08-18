"""Accounts exceptions module."""

from rest_framework import serializers


class InvalidBalance(serializers.ValidationError):
    """Exception raised when balance after transaction would turn negative."""

    def __init__(self, message, *args, **kwargs):
        detail = f"{message}"
        super().__init__(detail, *args, **kwargs)


class InvalidAccount(serializers.ValidationError):
    """Exception raised when given account is invalid."""

    def __init__(self, message, *args, **kwargs):
        detail = f"{message}"
        super().__init__(detail, *args, **kwargs)
