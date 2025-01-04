import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import redis
from app.core.config import settings

def test_database_connection():
    """
    Test the database connection
    """
    engine = create_engine(settings.DATABASE_URL)
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
