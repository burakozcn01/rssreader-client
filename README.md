# RSS Reader Client

[![PyPI version](https://badge.fury.io/py/rssreader-client.svg)](https://badge.fury.io/py/rssreader-client)
[![Python Versions](https://img.shields.io/pypi/pyversions/rssreader-client.svg)](https://pypi.org/project/rssreader-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern Python client library for the RSS Reader API.

## Features

- Full-featured client for the RSS Reader API
- Type hints for better IDE integration
- Comprehensive data models with proper typing
- Clean error handling with specific exceptions
- Simple and intuitive interface

## Installation

```bash
pip install rssreader-client
```

## Quick Start

```python
from rssreader import RSSClient

# Initialize the client
client = RSSClient("http://localhost:5000", "your-api-key")

# Get all categories
categories = client.get_categories()
for category in categories:
    print(f"{category.id}: {category.title} ({category.feed_count} feeds)")

# Get all feeds
feeds = client.get_feeds()
for feed in feeds:
    print(f"{feed.id}: {feed.title}")

# Get entries from a specific feed
result = client.get_feed_entries(feed_id=1)
for entry in result["entries"]:
    print(f"{entry.title} - {entry.published_at}")

# Get a specific entry with content
entry = client.get_entry(entry_id=42)
print(f"Title: {entry.title}")
print(f"Content: {entry.content[:100]}...")  # Show first 100 chars
```

## Documentation

### Client Class

#### `RSSClient(base_url, api_key)`

The main client for interacting with the RSS Reader API.

- `base_url`: Base URL of the RSS Reader API (e.g., "http://localhost:5000")
- `api_key`: API key for authentication

#### Methods

- `get_categories()` - Get all categories
- `get_feeds(category_id=None)` - Get all feeds, optionally filtered by category
- `get_entries(page=1, per_page=50, category_id=None, feed_id=None)` - Get entries with pagination
- `get_category_entries(category_id, page=1, per_page=50)` - Get entries for a specific category
- `get_feed_entries(feed_id, page=1, per_page=50)` - Get entries for a specific feed
- `get_entry(entry_id)` - Get a specific entry with content
- `get_status()` - Get system status
- `get_task_status()` - Get background task status

### Data Models

- `Category` - Represents a feed category
- `Feed` - Represents an RSS feed
- `Entry` - Represents a feed entry with content
- `SystemStatus` - System status information
- `TaskStatus` - Background task status
- `Pagination` - Pagination information

### Exception Classes

- `RSSReaderException` - Base exception
- `APIError` - API errors with status codes
- `AuthenticationError` - Authentication failures
- `ConnectionError` - Connection issues

## Examples

### Listing Categories and Feeds

```python
from rssreader import RSSClient

client = RSSClient("http://localhost:5000", "your-api-key")

# Get all categories
categories = client.get_categories()
print(f"Found {len(categories)} categories:")
for category in categories:
    print(f"  - {category.title} ({category.feed_count} feeds)")
    
    # Get feeds in this category
    feeds = client.get_feeds(category_id=category.id)
    for feed in feeds:
        print(f"    - {feed.title} ({feed.entry_count} entries)")
```

### Working with Entries

```python
from rssreader import RSSClient
from datetime import datetime, timedelta

client = RSSClient("http://localhost:5000", "your-api-key")

# Get recent entries (last 7 days)
result = client.get_entries(per_page=100)
entries = result["entries"]

# Filter for entries in the last 7 days
one_week_ago = datetime.now() - timedelta(days=7)
recent_entries = []

for entry in entries:
    published = entry.published_datetime()
    if published and published > one_week_ago:
        recent_entries.append(entry)

print(f"Found {len(recent_entries)} entries from the last 7 days:")
for entry in recent_entries[:5]:
    print(f"  - {entry.title}")
    print(f"    Published: {entry.published_at} | Feed: {entry.feed.get('title')}")
```

## License

MIT