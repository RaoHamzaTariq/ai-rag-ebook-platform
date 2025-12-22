import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_current_user_unauthorized(client):
    """Test that getting current user info requires authentication"""
    response = client.get("/users/me")

    # Should return 401 Unauthorized
    assert response.status_code == 401