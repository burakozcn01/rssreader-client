"""
Exception classes for the RSS Reader client.
"""

from typing import Optional


class RSSReaderException(Exception):
    """Base exception for RSS Reader client."""
    def __init__(self, message: str = "An error occurred with the RSS Reader client"):
        self.message = message
        super().__init__(self.message)


class APIError(RSSReaderException):
    """Exception raised for API errors."""
    def __init__(self, status_code: int, message: Optional[str] = None):
        self.status_code = status_code
        self.message = message or f"API Error (Status code: {status_code})"
        super().__init__(self.message)


class AuthenticationError(RSSReaderException):
    """Exception raised for authentication failures."""
    def __init__(self, message: str = "Authentication failed. Check your API key."):
        super().__init__(message)


class ConnectionError(RSSReaderException):
    """Exception raised for connection problems."""
    def __init__(self, message: str = "Failed to connect to the RSS Reader API"):
        super().__init__(message)