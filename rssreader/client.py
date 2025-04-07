"""
RSS Reader API client implementation.
"""

import requests
from typing import Dict, List, Optional, Union, Any

from .models import Category, Feed, Entry, SystemStatus, TaskStatus, Pagination
from .exceptions import APIError, AuthenticationError, ConnectionError


class RSSClient:
    """Client for interacting with the RSS Reader API."""

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the RSS Reader client.

        Args:
            base_url: Base URL of the RSS Reader API (e.g., "http://localhost:5000")
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }

    def _make_request(self, endpoint: str, method: str = "GET", 
                     params: Optional[Dict[str, Any]] = None, 
                     data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the API.

        Args:
            endpoint: API endpoint
            method: HTTP method
            params: Query parameters
            data: Request body data

        Returns:
            API response as a dictionary

        Raises:
            AuthenticationError: If authentication fails
            APIError: If the API returns an error
            ConnectionError: If there's a connection issue
        """
        url = f"{self.api_url}/{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                error_msg = "Invalid API key or authentication required"
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                except:
                    pass
                raise AuthenticationError(error_msg)
            
            error_msg = f"HTTP Error: {e.response.status_code}"
            try:
                error_data = e.response.json()
                if 'error' in error_data:
                    error_msg = error_data['error']
            except:
                pass
                
            raise APIError(e.response.status_code, error_msg)
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Connection error: {str(e)}")

    def get_categories(self) -> List[Category]:
        """
        Get all categories.

        Returns:
            List of Category objects
        """
        data = self._make_request("categories")
        return [Category.from_dict(item) for item in data]

    def get_feeds(self, category_id: Optional[int] = None) -> List[Feed]:
        """
        Get all feeds, optionally filtered by category.

        Args:
            category_id: Optional category ID filter

        Returns:
            List of Feed objects
        """
        params = {"category_id": category_id} if category_id else None
        data = self._make_request("feeds", params=params)
        return [Feed.from_dict(item) for item in data]

    def get_entries(self, page: int = 1, per_page: int = 50, 
                   category_id: Optional[int] = None, 
                   feed_id: Optional[int] = None) -> Dict[str, Union[List[Entry], Pagination]]:
        """
        Get entries, optionally filtered by category or feed.

        Args:
            page: Page number
            per_page: Entries per page
            category_id: Optional category ID filter
            feed_id: Optional feed ID filter

        Returns:
            Dictionary containing entries and pagination information
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        if category_id:
            params["category_id"] = category_id
        if feed_id:
            params["feed_id"] = feed_id
            
        data = self._make_request("entries", params=params)
        
        entries = [Entry.from_dict(item) for item in data.get('entries', [])]
        pagination = Pagination.from_dict(data.get('pagination', {}))
        
        return {
            "entries": entries,
            "pagination": pagination
        }

    def get_category_entries(self, category_id: int, page: int = 1, 
                            per_page: int = 50) -> Dict[str, Any]:
        """
        Get entries for a specific category.

        Args:
            category_id: Category ID
            page: Page number
            per_page: Entries per page

        Returns:
            Dictionary containing category info, entries, and pagination
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        data = self._make_request(f"categories/{category_id}/entries", params=params)
        
        entries = [Entry.from_dict(item) for item in data.get('entries', [])]
        pagination = Pagination.from_dict(data.get('pagination', {}))
        category = Category.from_dict(data.get('category', {})) if 'category' in data else None
        
        return {
            "category": category,
            "entries": entries,
            "pagination": pagination
        }

    def get_feed_entries(self, feed_id: int, page: int = 1, 
                        per_page: int = 50) -> Dict[str, Any]:
        """
        Get entries for a specific feed.

        Args:
            feed_id: Feed ID
            page: Page number
            per_page: Entries per page

        Returns:
            Dictionary containing feed info, entries, and pagination
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        data = self._make_request(f"feeds/{feed_id}/entries", params=params)
        
        entries = [Entry.from_dict(item) for item in data.get('entries', [])]
        pagination = Pagination.from_dict(data.get('pagination', {}))
        feed = Feed.from_dict(data.get('feed', {})) if 'feed' in data else None
        
        return {
            "feed": feed,
            "entries": entries,
            "pagination": pagination
        }

    def get_entry(self, entry_id: int) -> Entry:
        """
        Get a specific entry with its content.

        Args:
            entry_id: Entry ID

        Returns:
            Entry object with content and media
        """
        data = self._make_request(f"entries/{entry_id}")
        return Entry.from_dict(data)

    def get_status(self) -> SystemStatus:
        """
        Get system status.

        Returns:
            SystemStatus object
        """
        data = self._make_request("status")
        return SystemStatus.from_dict(data)

    def get_task_status(self) -> TaskStatus:
        """
        Get status of background tasks.

        Returns:
            TaskStatus object
        """
        data = self._make_request("task_status")
        return TaskStatus.from_dict(data)