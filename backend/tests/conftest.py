"""
Pytest configuration and fixtures
"""
import sys
import os
import pytest
import tempfile
from pathlib import Path

# Add the parent directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests

# Base URL for API testing
BASE_URL = "http://localhost:8081/api/v1"

@pytest.fixture
def test_user_data():
    """Create test user data"""
    return {
        "fullname": "Test User",
        "password": "password123",
        "email": "test@example.com"
    }

@pytest.fixture
def auth_client():
    """Create requests session with authentication"""
    session = requests.Session()
    # Don't set default Content-Type to allow multipart/form-data for file uploads
    session.headers.update({"Authorization": "Bearer test-token"})
    return session

@pytest.fixture
def client(auth_client):
    """Create standard requests session (authenticated)"""
    return auth_client
