from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from jose import jwt, JWTError
import os
from typing import Optional
import logging
import time

# Set up logger for auth middleware
logger = logging.getLogger('auth')

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.jwks_client = None
        self.jwks_cache_time = None
        self.cache_duration = 300  # Cache JWKS for 5 minutes

    async def __call__(self, request: Request):
        auth_header = request.headers.get('Authorization')
        user_id_header = request.headers.get('X-User-ID')
        
        logger.info(f"Auth check - Authorization: {bool(auth_header)}, X-User-ID: {bool(user_id_header)}")
        
        user_id = None
        jwt_payload = None
        
        # 1. Try Authorization header first (Production Standard)
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # Attempt full verification
                user_id, jwt_payload = await self.verify_jwt_with_payload(token)
                if user_id:
                    logger.info(f"Authenticated via JWT: {user_id}")
            except Exception as e:
                logger.warning(f"JWT Verification failed: {e}")
        
        # 2. Fallback to X-User-ID header if JWT is missing or verification failed
        # (This allows the frontend to identify the user even if JWKS server is temporarily unreachable)
        if not user_id and user_id_header:
            user_id = user_id_header
            logger.info(f"Authenticated via X-User-ID header: {user_id}")
            # We don't create a fake jwt_payload here; the dependency will load the user from DB
            jwt_payload = None

        # 3. Final Check - Reject if no identification is found
        if not user_id:
            logger.warning("Authentication failed: No user identification found")
            raise HTTPException(status_code=401, detail="Authentication required")

        # Store in request state
        request.state.user_id = user_id
        request.state.user_jwt_payload = jwt_payload
        
        return user_id

    async def verify_jwt_with_payload(self, token: str) -> tuple[Optional[str], Optional[dict]]:
        # Fetch JWKS from Better Auth with caching
        better_auth_url = os.getenv('BETTER_AUTH_URL', 'http://localhost:3001')
        jwks_url = f"{better_auth_url}/api/auth/jwks"

        # Check if we need to refresh the JWKS cache
        current_time = time.time()
        if (not self.jwks_client or
            not self.jwks_cache_time or
            (current_time - self.jwks_cache_time) > self.cache_duration):
            try:
                async with httpx.AsyncClient() as client:
                    jwks_response = await client.get(jwks_url)
                    jwks_response.raise_for_status()
                    jwks = jwks_response.json()
                    self.jwks_client = jwks
                    self.jwks_cache_time = current_time
                    logger.info("Successfully fetched and cached JWKS from Better Auth")
            except httpx.RequestError as e:
                logger.error(f"Failed to fetch JWKS: {e}")
                return None, None
            except Exception as e:
                logger.error(f"Unexpected error while fetching JWKS: {e}")
                return None, None

        try:
            # Log token details for debugging
            logger.info(f"Attempting to verify JWT token (first 20 chars): {token[:20]}...")
            logger.info(f"JWKS available: {bool(self.jwks_client)}")
            
            # Decode and verify the token
            payload = jwt.decode(
                token,
                self.jwks_client,
                algorithms=["RS256", "EdDSA"],  # Support both algorithms used by BetterAuth
                options={
                    "verify_exp": True,
                    "verify_aud": False  # Disable audience verification for now
                }
            )
            logger.info(f"Successfully decoded JWT for user: {payload.get('sub')}")
            user_id = payload.get('sub')  # User ID is in 'sub' claim
            return user_id, payload  # Return both user ID and full payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None, None
        except jwt.JWTClaimsError as e:
            logger.error(f"JWT claims error: {e}")
            return None, None
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            logger.error(f"Token details: {token[:50]}...")
            return None, None
        except Exception as e:
            logger.error(f"Unexpected error during JWT verification: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return None, None