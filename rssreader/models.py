"""
Data models for the RSS Reader API.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union, Any, ClassVar


@dataclass
class Category:
    """Represents a feed category"""
    id: int
    title: str
    feed_count: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Category':
        """Create a Category from a dictionary"""
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            feed_count=data.get('feed_count', 0)
        )


@dataclass
class Feed:
    """Represents an RSS feed"""
    id: int
    title: str
    site_url: Optional[str]
    feed_url: str
    category: Optional[Dict[str, Union[int, str]]]
    checked_at: Optional[str]
    disabled: bool
    parsing_error_count: int
    entry_count: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feed':
        """Create a Feed from a dictionary"""
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            site_url=data.get('site_url'),
            feed_url=data.get('feed_url'),
            category=data.get('category'),
            checked_at=data.get('checked_at'),
            disabled=data.get('disabled', False),
            parsing_error_count=data.get('parsing_error_count', 0),
            entry_count=data.get('entry_count', 0)
        )


@dataclass
class Entry:
    """Represents an entry from an RSS feed"""
    id: int
    feed_id: int
    title: str
    url: str
    published_at: Optional[str]
    created_at: str
    author: Optional[str]
    feed: Dict[str, Any]
    content: Optional[str] = None
    media: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entry':
        """Create an Entry from a dictionary"""
        return cls(
            id=data.get('id'),
            feed_id=data.get('feed_id'),
            title=data.get('title'),
            url=data.get('url'),
            published_at=data.get('published_at'),
            created_at=data.get('created_at'),
            author=data.get('author'),
            feed=data.get('feed', {}),
            content=data.get('content'),
            media=data.get('media')
        )

    def published_datetime(self) -> Optional[datetime]:
        """Return the published date as a datetime object"""
        if not self.published_at:
            return None
        return datetime.fromisoformat(self.published_at.replace('Z', '+00:00'))


@dataclass
class Pagination:
    """Represents pagination information"""
    page: int
    per_page: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pagination':
        """Create a Pagination from a dictionary"""
        return cls(
            page=data.get('page', 1),
            per_page=data.get('per_page', 50),
            total=data.get('total', 0),
            pages=data.get('pages', 1),
            has_next=data.get('has_next', False),
            has_prev=data.get('has_prev', False)
        )


@dataclass
class SystemStatus:
    """Represents the system status"""
    feed_count: int
    category_count: int
    entry_count: int
    latest_checked: Optional[str]
    latest_entry: Optional[str]
    update_interval: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemStatus':
        """Create a SystemStatus from a dictionary"""
        return cls(
            feed_count=data.get('feeds', {}).get('total', 0),
            category_count=data.get('categories', {}).get('total', 0),
            entry_count=data.get('entries', {}).get('total', 0),
            latest_checked=data.get('feeds', {}).get('latest_checked'),
            latest_entry=data.get('entries', {}).get('latest'),
            update_interval=data.get('update_interval', 0)
        )


@dataclass
class TaskStatus:
    """Represents the status of background tasks"""
    feed_tasks: Dict[int, bool]
    all_feeds_running: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskStatus':
        """Create a TaskStatus from a dictionary"""
        feed_tasks = {}
        all_feeds_running = False

        for key, task in data.items():
            if key == 'all_feeds':
                all_feeds_running = task.get('running', False)
            elif key.startswith('feed_'):
                try:
                    feed_id = int(key.split('_')[1])
                    feed_tasks[feed_id] = task.get('running', False)
                except (IndexError, ValueError):
                    pass

        return cls(
            feed_tasks=feed_tasks,
            all_feeds_running=all_feeds_running
        )