import pytest
import tempfile
import os
import io
import logging
import requests
from conftest import BASE_URL


logger = logging.getLogger(__name__)


@pytest.fixture
def sample_file_content():
    """Create sample file content for testing"""
    return b"This is a test file content for API testing."


@pytest.fixture
def sample_text_file(sample_file_content):
    """Create a temporary text file for testing"""
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
        f.write(sample_file_content)
        f.flush()
        yield f.name
    # Cleanup
    if os.path.exists(f.name):
        os.unlink(f.name)


def test_upload_file_success(client, sample_text_file):
    """Test successful file upload"""
    url = f"{BASE_URL}/file/upload"
    
    with open(sample_text_file, 'rb') as f:
        files = {'file': ('test_file.txt', f, 'text/plain')}
        data = {'path': '/tmp/test_file.txt'}
        response = client.post(url, files=files, data=data)
    
    logger.info(f"Upload file response: {response.status_code} - {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'message' in data
    assert 'data' in data


def test_upload_file_without_file(client):
    """Test upload without providing file"""
    url = f"{BASE_URL}/file/upload"
    response = client.post(url)
    
    logger.info(f"Upload without file response: {response.status_code} - {response.text}")
    assert response.status_code == 422  # Validation error


def test_upload_empty_file(client):
    """Test upload empty file"""
    url = f"{BASE_URL}/file/upload"
    
    # Create empty file
    empty_file = io.BytesIO(b"")
    files = {'file': ('empty.txt', empty_file, 'text/plain')}
    data = {'path': '/tmp/empty.txt'}
    response = client.post(url, files=files, data=data)
    
    logger.info(f"Upload empty file response: {response.status_code} - {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'message' in data
    assert 'data' in data


def test_read_file_success(client, sample_text_file):
    """Test getting file content"""
    # First upload a file
    upload_url = f"{BASE_URL}/file/upload"
    with open(sample_text_file, 'rb') as f:
        files = {'file': ('info_test.txt', f, 'text/plain')}
        data = {'path': '/tmp/info_test.txt'}
        upload_response = client.post(upload_url, files=files, data=data)
    
    logger.info(f"Upload for read test response: {upload_response.status_code} - {upload_response.text}")
    assert upload_response.status_code == 200
    
    # Read file
    read_url = f"{BASE_URL}/file/read"
    read_data = {'file': '/tmp/info_test.txt'}
    response = client.post(read_url, json=read_data)
    
    logger.info(f"Read file response: {response.status_code} - {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'message' in data
    assert 'data' in data


def test_read_file_not_found(client):
    """Test reading non-existent file"""
    url = f"{BASE_URL}/file/read"
    data = {'file': '/tmp/nonexistent.txt'}
    response = client.post(url, json=data)
    
    logger.info(f"Read file not found response: {response.status_code} - {response.text}")
    assert response.status_code == 404  # File not found


def test_delete_file_success(client, sample_text_file):
    """Test successful file deletion"""
    # First upload a file
    upload_url = f"{BASE_URL}/file/upload"
    with open(sample_text_file, 'rb') as f:
        files = {'file': ('delete_test.txt', f, 'text/plain')}
        data = {'path': '/tmp/delete_test.txt'}
        upload_response = client.post(upload_url, files=files, data=data)
    
    logger.info(f"Upload for delete test response: {upload_response.status_code} - {upload_response.text}")
    assert upload_response.status_code == 200
    
    # Delete file
    delete_url = f"{BASE_URL}/file/delete"
    delete_data = {'file': '/tmp/delete_test.txt'}  # Use file instead of path
    response = client.post(delete_url, json=delete_data)
    
    logger.info(f"Delete file response: {response.status_code} - {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'message' in data
    assert 'data' in data
    
    # Verify file is deleted by trying to read it
    read_url = f"{BASE_URL}/file/read"
    read_data = {'file': '/tmp/delete_test.txt'}
    read_response = client.post(read_url, json=read_data)
    logger.info(f"Verify deletion response: {read_response.status_code} - {read_response.text}")
    assert read_response.status_code == 404  # File not found


def test_delete_file_not_found(client):
    """Test deleting non-existent file"""
    url = f"{BASE_URL}/file/delete"
    data = {'file': '/tmp/nonexistent.txt'}  # Use file instead of path
    response = client.post(url, json=data)
    
    logger.info(f"Delete file not found response: {response.status_code} - {response.text}")
    assert response.status_code == 404  # File not found


def test_upload_large_file(client):
    """Test uploading a larger file"""
    # Create a 1MB file content
    large_content = b"A" * (1024 * 1024)  # 1MB
    
    url = f"{BASE_URL}/file/upload"
    files = {'file': ('large_file.txt', io.BytesIO(large_content), 'text/plain')}
    data = {'path': '/tmp/large_file.txt'}
    response = client.post(url, files=files, data=data)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'message' in data
    assert 'data' in data


def test_upload_binary_file(client):
    """Test uploading a binary file"""
    # Create binary content
    binary_content = bytes(range(256))  # 0-255 bytes
    
    url = f"{BASE_URL}/file/upload"
    files = {'file': ('binary_file.bin', io.BytesIO(binary_content), 'application/octet-stream')}
    data = {'path': '/tmp/binary_file.bin'}
    response = client.post(url, files=files, data=data)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'message' in data
    assert 'data' in data
    
    # Download and verify content
    download_url = f"{BASE_URL}/file/download"
    params = {'path': '/tmp/binary_file.bin'}
    download_response = client.get(download_url, params=params)
    
    assert download_response.status_code == 200
    assert download_response.content == binary_content

