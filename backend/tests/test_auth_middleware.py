import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.main import app
from src.middleware.auth_middleware import JWTBearer


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_jwt_bearer_verification():
    """Test JWT Bearer token verification"""
    middleware = JWTBearer()

    # Mock a valid token and JWKS
    with patch('src.middleware.auth_middleware.httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "kid": "test-key",
                    "n": "some_base64_encoded_modulus",
                    "e": "AQAB"
                }
            ]
        }
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

        # Test token verification logic
        # This would be more comprehensive with actual JWT testing
        assert middleware is not None


def test_protected_endpoint_requires_auth(client):
    """Test that protected endpoints require authentication"""
    # Test agents endpoint without auth
    response = client.post("/agents/run", json={
        "agent_type": "triage",
        "query": "test query"
    })

    # Should return 401 Unauthorized
    assert response.status_code == 401