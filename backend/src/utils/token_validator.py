from jose import jwt, JWTError
import os
from typing import Optional, Dict, Any
import logging

# Set up logger
logger = logging.getLogger('auth')

async def validate_token_structure(token: str) -> bool:
    """
    Validates the basic structure of a JWT token (header.payload.signature format)
    without verifying its signature or claims.
    """
    try:
        # Split the token into its three parts
        parts = token.split('.')
        if len(parts) != 3:
            logger.warning("Token does not have the correct number of parts")
            return False

        # Check if each part is properly base64 encoded
        for part in parts:
            # Decode the part to check if it's valid base64
            import base64
            try:
                # Add padding if needed
                padded_part = part + '=' * (4 - len(part) % 4)
                base64.b64decode(padded_part)
            except Exception:
                logger.warning(f"Invalid base64 encoding in token part: {part[:10]}...")
                return False

        logger.info("Token structure validation passed")
        return True
    except Exception as e:
        logger.error(f"Error during token structure validation: {e}")
        return False

async def extract_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Extracts the payload from a JWT token without verifying its signature.
    Use this carefully - only for tokens you trust.
    """
    try:
        # Split the token and decode the payload part
        parts = token.split('.')
        if len(parts) != 3:
            logger.warning("Invalid token format")
            return None

        import base64
        payload_part = parts[1]

        # Add padding if needed
        padded_payload = payload_part + '=' * (4 - len(payload_part) % 4)

        # Decode the payload
        decoded_payload = base64.b64decode(padded_payload)

        # Parse as JSON
        import json
        payload = json.loads(decoded_payload)

        logger.info("Successfully extracted token payload")
        return payload
    except Exception as e:
        logger.error(f"Error extracting token payload: {e}")
        return None

async def is_token_expired(token: str) -> bool:
    """
    Checks if a token is expired by examining its 'exp' claim.
    This does not verify the token signature.
    """
    payload = await extract_token_payload(token)
    if not payload:
        logger.warning("Could not extract payload to check expiration")
        return True  # Assume expired if we can't check

    import time
    exp = payload.get('exp')
    if not exp:
        logger.info("No expiration claim found in token")
        return False  # No expiration claim means it doesn't expire

    current_time = int(time.time())
    is_expired = current_time > exp

    if is_expired:
        logger.info("Token is expired")
    else:
        logger.info("Token is not expired")

    return is_expired

async def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extracts the user ID (sub claim) from a token without verifying its signature.
    Use this carefully - only for tokens you trust.
    """
    payload = await extract_token_payload(token)
    if not payload:
        logger.warning("Could not extract payload to get user ID")
        return None

    user_id = payload.get('sub')
    logger.info(f"Extracted user ID from token: {user_id}")
    return user_id

def get_better_auth_public_key():
    """
    Returns the public key configuration for Better Auth tokens.
    This is used for verification in the middleware.
    """
    # This function would typically fetch the public key from Better Auth
    # In practice, this is handled by the JWKS fetching in the middleware
    audience = os.getenv('BETTER_AUTH_AUDIENCE', 'your-app-audience')
    issuer = os.getenv('BETTER_AUTH_URL', 'http://localhost:3000')

    return {
        'audience': audience,
        'issuer': issuer
    }