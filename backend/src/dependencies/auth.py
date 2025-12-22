from fastapi import Depends, HTTPException, Request
from typing import Optional
import logging
from ..middleware.auth_middleware import JWTBearer
from ..services.user_service import UserService
from ..config.database import get_sync_db
from sqlmodel import Session

# Set up logger
logger = logging.getLogger('auth')

# Initialize the JWT Bearer authentication scheme
oauth2_scheme = JWTBearer(auto_error=True)

async def get_current_user_id(request: Request, _ = Depends(oauth2_scheme)) -> str:
    """
    Dependency to get the user ID from the request state.
    Always returns a value (either real user ID or a fallback).
    """
    try:
        # The user_id should have been set in the request state by the JWTBearer middleware
        user_id = getattr(request.state, 'user_id', None)
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Authentication required")
        jwt_payload = getattr(request.state, 'user_jwt_payload', None)

        # Sync user data from JWT/state if available
        if jwt_payload:
            try:
                # Get database session to sync user data
                with next(get_sync_db()) as session:
                    await UserService.get_or_create_user_from_jwt_payload(session, jwt_payload)
            except Exception as e:
                logger.warning(f"Could not sync user data: {e}")

        logger.info(f"Using User ID for request: {user_id}")
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user_id dependency: {e}")
        raise HTTPException(status_code=401, detail="Authentication error")

async def get_optional_user_id(request: Request, _ = Depends(oauth2_scheme)) -> Optional[str]:
    """
    Dependency to get the current user's ID if authenticated, or None if not.
    This is useful for endpoints that work differently if a user is authenticated.
    """
    try:
        user_id = getattr(request.state, 'user_id', None)
        jwt_payload = getattr(request.state, 'user_jwt_payload', None)

        if user_id and jwt_payload:
            try:
                # Get database session to sync user data
                with next(get_sync_db()) as session:  # Using sync db as we're in a sync context
                    await UserService.get_or_create_user_from_jwt_payload(session, jwt_payload)
            except Exception as e:
                logger.warning(f"Could not sync user data from JWT: {e}")

        if user_id:
            logger.info(f"Optional user ID retrieved: {user_id}")

        return user_id
    except Exception as e:
        logger.warning(f"Error retrieving optional user ID: {e}")
        return None