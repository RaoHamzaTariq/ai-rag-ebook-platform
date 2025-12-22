"""
Token utility functions for introspection that don't compromise security.
These functions provide safe ways to examine token properties without bypassing validation.
"""
from typing import Optional, Dict, Any
import logging
import time
import base64
import json

logger = logging.getLogger('auth')

def extract_token_payload_unverified(token: str) -> Optional[Dict[str, Any]]:
    """
    Extracts the payload from a JWT token WITHOUT verifying its signature.
    Use this carefully - only for tokens you trust or for debugging purposes.
    This does NOT validate the token, so don't use it for authentication decisions.
    """
    try:
        # Split the token into its three parts (header.payload.signature)
        parts = token.split('.')
        if len(parts) != 3:
            logger.warning("Token does not have the correct number of parts")
            return None

        payload_part = parts[1]

        # Add padding if needed (JWT uses base64url encoding which omits padding)
        padded_payload = payload_part + '=' * (4 - len(payload_part) % 4)

        # Decode the payload
        decoded_payload = base64.urlsafe_b64decode(padded_payload)

        # Parse as JSON
        payload = json.loads(decoded_payload)

        logger.info("Successfully extracted token payload for introspection")
        return payload
    except Exception as e:
        logger.error(f"Error extracting token payload: {e}")
        return None

def is_token_expired_unverified(token: str) -> bool:
    """
    Checks if a token is expired by examining its 'exp' claim.
    This does not verify the token signature - use only for trusted tokens.
    """
    payload = extract_token_payload_unverified(token)
    if not payload:
        logger.warning("Could not extract payload to check expiration")
        return True  # Assume expired if we can't check

    exp = payload.get('exp')
    if not exp:
        logger.info("No expiration claim found in token")
        return False  # No expiration claim means it doesn't expire

    current_time = int(time.time())
    is_expired = current_time > exp

    if is_expired:
        logger.info("Token is expired based on exp claim")
    else:
        logger.info("Token is not expired based on exp claim")

    return is_expired

def get_user_info_from_token_unverified(token: str) -> Optional[Dict[str, Any]]:
    """
    Extracts user-related information (sub, email, name) from a token.
    This does not verify the token signature - use only for trusted tokens.
    """
    payload = extract_token_payload_unverified(token)
    if not payload:
        logger.warning("Could not extract payload to get user info")
        return None

    user_info = {
        'sub': payload.get('sub'),
        'email': payload.get('email'),
        'name': payload.get('name'),
        'iat': payload.get('iat'),
        'exp': payload.get('exp')
    }

    logger.info(f"Extracted user info from token: {user_info['sub']}")
    return user_info

def validate_token_structure(token: str) -> bool:
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

        # Check if each part is properly base64url encoded
        for i, part in enumerate(parts):
            if not part:  # Empty part is invalid
                logger.warning(f"Token part {i} is empty")
                return False

            # Check if it contains valid base64url characters
            import re
            if not re.match(r'^[A-Za-z0-9_-]+$', part):
                logger.warning(f"Invalid characters in token part {i}")
                return False

        logger.info("Token structure validation passed")
        return True
    except Exception as e:
        logger.error(f"Error during token structure validation: {e}")
        return False