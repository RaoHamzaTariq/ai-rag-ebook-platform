import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_user_conversations_unauthorized(client):
    """Test that getting user conversations requires authentication"""
    response = client.get("/conversations/")

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_get_conversation_by_id_unauthorized(client):
    """Test that getting a specific conversation requires authentication"""
    response = client.get("/conversations/test-id")

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_get_conversation_messages_unauthorized(client):
    """Test that getting conversation messages requires authentication"""
    response = client.get("/conversations/test-id/messages")

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_create_conversation_message_unauthorized(client):
    """Test that creating a conversation message requires authentication"""
    response = client.post("/conversations/test-id/messages", json={
        "role": "user",
        "content": "test message"
    })

    # Should return 401 Unauthorized
    assert response.status_code == 401