from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from typing import Optional
import logging

# Set up logger for auth middleware
logger = logging.getLogger('auth')

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        user_id_header = request.headers.get('X-User-ID')

        logger.info(f"Auth check - X-User-ID: {bool(user_id_header)}")

        # Only use X-User-ID header for authentication (JWT logic removed)
        if user_id_header:
            user_id = user_id_header
            logger.info(f"Authenticated via X-User-ID header: {user_id}")
        else:
            logger.warning("Authentication failed: No user identification found")
            raise HTTPException(status_code=401, detail="Authentication required")

        # Store in request state
        request.state.user_id = user_id
        request.state.user_jwt_payload = None  # No JWT payload since JWT logic is removed

        return user_id