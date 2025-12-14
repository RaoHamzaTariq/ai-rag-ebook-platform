from fastapi import Depends, HTTPException, Request
from typing import Optional
import logging
from ..middleware.auth_middleware import JWTBearer

# Set up logger
logger = logging.getLogger('auth')

# Initialize the JWT Bearer authentication scheme
oauth2_scheme = JWTBearer(auto_error=True)

async def get_current_user_id(request: Request) -> str:
    """
    Dependency to get the current authenticated user's ID from the request state.
    This function is called by endpoints that require authentication.
    """
    try:
        # The user_id should have been set in the request state by the JWTBearer middleware
        user_id = getattr(request.state, 'user_id', None)

        if not user_id:
            logger.warning("Attempt to access protected endpoint without valid user ID in request state")
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

        logger.info(f"Retrieved authenticated user ID: {user_id}")
        return user_id
    except Exception as e:
        logger.error(f"Error retrieving current user ID: {e}")
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

async def get_optional_user_id(request: Request) -> Optional[str]:
    """
    Dependency to get the current user's ID if authenticated, or None if not.
    This is useful for endpoints that work differently for authenticated vs anonymous users.
    """
    try:
        user_id = getattr(request.state, 'user_id', None)

        if user_id:
            logger.info(f"Optional user ID retrieved: {user_id}")

        return user_id
    except Exception as e:
        logger.warning(f"Error retrieving optional user ID: {e}")
        return None