"""Module for pypetwalk Exceptions."""
from __future__ import annotations

from typing import Any


class BasePyPetWALKException(Exception):
    """pypetwalk Base exception."""

    def __init__(self, name: str, *args: Any) -> None:
        """Init the BasePyPetWALKException."""
        super().__init__(*args)
        self.name = name


class PyPetWALKUnknownStateError(BasePyPetWALKException):
    """pypetwalk PyPetWALKUnknownStateError exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyPetWALKUnknownStateError."""
        super().__init__("PyPetWALKUnknownStateError", *args)


class PyPetWALKClientConnectionError(BasePyPetWALKException):
    """pypetwalk PyPetWALKClientConnectionError exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyPetWALKClientConnectionError."""
        super().__init__("PyPetWALKClientConnectionError", *args)


class PyPetWALKInvalidResponse(BasePyPetWALKException):
    """pypetwalk PyPetWALKInvalidResponse exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyPetWALKInvalidResponse."""
        super().__init__("PyPetWALKInvalidResponse", *args)


class PyPetWALKInvalidResponseValue(BasePyPetWALKException):
    """pypetwalk PyPetWALKInvalidResponseValue exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyPetWALKInvalidResponseValue."""
        super().__init__("PyPetWALKInvalidResponseValue", *args)


class PyPetWALKInvalidResponseStatus(BasePyPetWALKException):
    """pypetwalk PyPetWALKInvalidResponseStatus exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyPetWALKInvalidResponseStatus."""
        super().__init__("PyPetWALKInvalidResponseStatus", *args)


class PyPetWALKClientAWSAuthenticationError(BasePyPetWALKException):
    """pypetwalk PyPetWALKClientAWSAuthenticationError exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyPetWALKClientAWSAuthenticationError."""
        super().__init__("PyPetWALKClientAWSAuthenticationError", *args)


class PyPetWALKClientAWSInvalidTokens(BasePyPetWALKException):
    """pypetwalk PyPetWALKClientAWSInvalidTokens exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyPetWALKClientAWSInvalidTokens."""
        super().__init__("PyPetWALKClientAWSInvalidTokens", *args)
