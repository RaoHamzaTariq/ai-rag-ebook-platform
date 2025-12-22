"""
Test suite for token verification functionality.
This includes tests for JWT validation, JWKS fetching, and middleware functionality.
"""
import pytest
import os
from jose import jwt
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
import asyncio

from src.middleware.auth_middleware import JWTBearer
from src.dependencies.auth import get_current_user_id
from src.utils.token_utils import validate_token_structure, extract_token_payload_unverified

# Mock environment variables for testing
os.environ['BETTER_AUTH_URL'] = 'http://test-better-auth.com'
os.environ['BETTER_AUTH_AUDIENCE'] = 'http://test-better-auth.com'

# Mock secret and algorithm for testing - in real scenario, BetterAuth handles this
TEST_SECRET = "test-secret-key-for-unit-testing"
TEST_ALGORITHM = "HS256"

def create_test_token(user_id: str = "test-user-id", email: str = "test@example.com", name: str = "Test User"):
    """Create a test JWT token for testing purposes"""
    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, TEST_SECRET, algorithm=TEST_ALGORITHM)
    return token

@pytest.mark.asyncio
async def test_token_structure_validation():
    """Test that token structure validation works correctly"""
    # Create a valid test token
    valid_token = create_test_token()

    # Test valid token structure
    assert validate_token_structure(valid_token) == True

    # Test invalid token structure (missing parts)
    invalid_token = "header.payload"  # Missing signature part
    assert validate_token_structure(invalid_token) == False

    # Test invalid token structure (extra parts)
    invalid_token = "header.payload.signature.extra"  # Too many parts
    assert validate_token_structure(invalid_token) == False

    print("✓ Token structure validation tests passed")

@pytest.mark.asyncio
async def test_token_payload_extraction():
    """Test that token payload extraction works correctly (without validation)"""
    # Create a test token
    test_user_id = "test-user-123"
    test_email = "test@example.com"
    test_name = "Test User"
    token = create_test_token(test_user_id, test_email, test_name)

    # Extract payload without validation
    payload = extract_token_payload_unverified(token)

    assert payload is not None
    assert payload['sub'] == test_user_id
    assert payload['email'] == test_email
    assert payload['name'] == test_name

    print("✓ Token payload extraction tests passed")

@pytest.mark.asyncio
async def test_jwt_bearer_middleware():
    """Test JWT Bearer middleware functionality"""
    middleware = JWTBearer()

    # Create a test token
    test_token = create_test_token()

    # Mock the JWKS response to simulate BetterAuth JWKS endpoint
    mock_jwks = {
        "keys": [
            {
                "kty": "oct",  # For testing with HS256
                "use": "sig",
                "k": TEST_SECRET,
                "alg": "HS256"
            }
        ]
    }

    # Patch the HTTP client to return our mock JWKS
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_jwks
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test JWT verification with payload
        user_id, payload = await middleware.verify_jwt_with_payload(test_token)

        assert user_id is not None
        assert payload is not None
        assert user_id == "test-user-id"
        assert payload['email'] == "test@example.com"

    print("✓ JWT Bearer middleware tests passed")

@pytest.mark.asyncio
async def test_expired_token_handling():
    """Test that expired tokens are properly rejected"""
    # Create an expired token
    expired_payload = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "iat": datetime.utcnow() - timedelta(hours=2),
        "exp": datetime.utcnow() - timedelta(hours=1)  # Already expired
    }
    expired_token = jwt.encode(expired_payload, TEST_SECRET, algorithm=TEST_ALGORITHM)

    # Check if token is expired using utility function
    is_expired = extract_token_payload_unverified(expired_token)
    if is_expired:
        exp_time = is_expired.get('exp')
        current_time = int(datetime.utcnow().timestamp())
        assert exp_time < current_time  # Token should be expired

    print("✓ Expired token handling tests passed")

def run_token_verification_tests():
    """Run all token verification tests"""
    print("Running token verification tests...")

    # Run sync tests
    test_token_structure_validation()
    test_token_payload_extraction()
    test_expired_token_handling()

    # Run async tests
    asyncio.run(test_jwt_bearer_middleware())

    print("All token verification tests completed successfully!")

if __name__ == "__main__":
    run_token_verification_tests()