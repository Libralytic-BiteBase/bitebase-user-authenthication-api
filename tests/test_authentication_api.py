import sys
import os
import pytest
from unittest.mock import patch
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import redis

# Ensure the app module is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.auth import authenticate_user, get_facebook_user, get_google_user
from app.core.config import settings

# Authentication tests
@patch('app.core.auth.requests.post')
def test_authenticate_user_success(mock_post):
    # Arrange
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'token': 'fake_token'}

    # Act
    response = authenticate_user('test_user', 'test_password')

    # Assert
    assert response['token'] == 'fake_token'
    mock_post.assert_called_once()

@patch('app.core.auth.requests.post')
def test_authenticate_user_failure(mock_post):
    # Arrange
    mock_post.return_value.status_code = 401

    # Act
    response = authenticate_user('test_user', 'wrong_password')

    # Assert
    assert response is None
    mock_post.assert_called_once()

@patch('app.core.auth.requests.post')
def test_authenticate_user_invalid_response(mock_post):
    # Arrange
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {}

    # Act
    response = authenticate_user('test_user', 'test_password')

    # Assert
    assert response is None
    mock_post.assert_called_once()

@patch('app.core.auth.requests.get')
def test_get_facebook_user_success(mock_get):
    # Arrange
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'id': '12345',
        'name': 'Test User',
        'email': 'test@example.com'
    }

    # Act
    response = get_facebook_user('fake_token')

    # Assert
    assert response['id'] == '12345'
    assert response['name'] == 'Test User'
    mock_get.assert_called_once()

@patch('app.core.auth.requests.get')
def test_get_facebook_user_failure(mock_get):
    # Arrange
    mock_get.return_value.status_code = 401

    # Act
    response = get_facebook_user('fake_token')

    # Assert
    assert response is None
    mock_get.assert_called_once()

@patch('app.core.auth.requests.get')
def test_get_facebook_user_invalid_response(mock_get):
    # Arrange
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}

    # Act
    response = get_facebook_user('fake_token')

    # Assert
    assert response is None
    mock_get.assert_called_once()

@patch('app.core.auth.requests.get')
def test_get_google_user_success(mock_get):
    # Arrange
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'sub': '12345',
        'name': 'Test User',
        'email': 'test@example.com'
    }

    # Act
    response = get_google_user('fake_token')

    # Assert
    assert response['sub'] == '12345'
    assert response['name'] == 'Test User'
    mock_get.assert_called_once()

@patch('app.core.auth.requests.get')
def test_get_google_user_failure(mock_get):
    # Arrange
    mock_get.return_value.status_code = 401

    # Act
    response = get_google_user('fake_token')

    # Assert
    assert response is None
    mock_get.assert_called_once()

@patch('app.core.auth.requests.get')
def test_get_google_user_invalid_response(mock_get):
    # Arrange
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}

    # Act
    response = get_google_user('fake_token')

    # Assert
    assert response is None
    mock_get.assert_called_once()

def test_authenticate_user_exception():
    # Test handling of exceptions
    with patch('app.core.auth.requests.post') as mock_post:
        mock_post.side_effect = Exception("Connection error")
        response = authenticate_user('test_user', 'test_password')
        assert response is None

def test_get_facebook_user_exception():
    # Test handling of exceptions
    with patch('app.core.auth.requests.get') as mock_get:
        mock_get.side_effect = Exception("API error")
        response = get_facebook_user('fake_token')
        assert response is None

def test_get_google_user_exception():
    # Test handling of exceptions
    with patch('app.core.auth.requests.get') as mock_get:
        mock_get.side_effect = Exception("API error")
        response = get_google_user('fake_token')
        assert response is None

# Service status tests
def test_database_connection():
    """
    Test the database connection
    """
    engine = create_engine(settings.DATABASE_URL, connect_args={"sslmode": "require"})
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            assert result.fetchone()[0] == 1
    except OperationalError as e:
        pytest.fail(f"Database connection failed: {e}")

def test_redis_connection():
    """
    Test the Redis server connection
    """
    try:
        r = redis.StrictRedis.from_url(settings.REDIS_URL)
        response = r.ping()
        assert response is True
    except redis.ConnectionError as e:
        pytest.fail(f"Redis connection failed: {e}")

# Simulate database and Redis server being inaccessible
@patch('sqlalchemy.create_engine')
def test_database_connection_failure(mock_create_engine):
    """
    Test the database connection failure
    """
    mock_create_engine.side_effect = OperationalError("Mocked connection error", None, None)
    with pytest.raises(OperationalError):
        engine = create_engine(settings.DATABASE_URL, connect_args={"sslmode": "require"})
        with engine.connect() as connection:
            connection.execute("SELECT 1")

@patch('redis.StrictRedis.ping')
def test_redis_connection_failure(mock_ping):
    """
    Test the Redis server connection failure
    """
    mock_ping.side_effect = redis.ConnectionError("Mocked connection error")
    with pytest.raises(redis.ConnectionError):
        r = redis.StrictRedis.from_url(settings.REDIS_URL)
        r.ping()

# Database interaction tests
def test_insert_and_retrieve_user():
    """
    Test inserting and retrieving a user from the database
    """
    engine = create_engine(settings.DATABASE_URL, connect_args={"sslmode": "require"})
    try:
        with engine.connect() as connection:
            # Insert a user
            connection.execute(
                text("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)"),
                {"username": "testuser", "password": "password123", "email": "test@example.com"}
            )
            # Retrieve the user
            result = connection.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {"email": "test@example.com"}
            )
            user = result.fetchone()
            assert user is not None
            assert user['username'] == 'testuser'
            assert user['email'] == 'test@example.com'
    except OperationalError as e:
        pytest.fail(f"Database interaction failed: {e}")