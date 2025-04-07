"""
RSS Reader Client - Python client for RSS Reader API
"""

from .client import RSSClient
from .models import Category, Feed, Entry, SystemStatus, TaskStatus, Pagination
from .exceptions import (
    RSSReaderException,
    APIError,
    AuthenticationError,
    ConnectionError
)

__version__ = '0.1.0'
__all__ = [
    'RSSClient',
    'Category',
    'Feed',
    'Entry',
    'SystemStatus',
    'TaskStatus',
    'Pagination',
    'RSSReaderException',
    'APIError',
    'AuthenticationError',
    'ConnectionError'
]