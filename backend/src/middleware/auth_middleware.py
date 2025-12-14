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
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                logger.warning(f"Invalid authentication scheme: {credentials.scheme}")
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")

            token = credentials.credentials
            user_id = await self.verify_jwt(token)
            if not user_id:
                logger.warning("Invalid token or expired token")
                raise HTTPException(status_code=401, detail="Invalid token or expired token.")

            # Store user_id in request state for use in endpoints
            request.state.user_id = user_id
            logger.info(f"Successfully authenticated user: {user_id}")
            return credentials.credentials
        else:
            logger.warning("No authorization credentials provided")
            raise HTTPException(status_code=401, detail="Not authenticated.")

    async def verify_jwt(self, token: str) -> Optional[str]:
        # Fetch JWKS from Better Auth with caching
        better_auth_url = os.getenv('BETTER_AUTH_URL', 'http://localhost:3000')
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
                return None
            except Exception as e:
                logger.error(f"Unexpected error while fetching JWKS: {e}")
                return None

        try:
            # Decode and verify the token
            payload = jwt.decode(
                token,
                self.jwks_client,
                algorithms=["RS256"],
                audience=os.getenv('BETTER_AUTH_AUDIENCE', 'your-app-audience'),
                options={"verify_exp": True}  # Verify token expiration
            )
            logger.info(f"Successfully decoded JWT for user: {payload.get('sub')}")
            return payload.get('sub')  # User ID is in 'sub' claim
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.JWTClaimsError as e:
            logger.error(f"JWT claims error: {e}")
            return None
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during JWT verification: {e}")
            return None