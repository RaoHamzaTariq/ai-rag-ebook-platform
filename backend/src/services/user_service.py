from sqlmodel import Session, select
from ..models.user import User
from typing import Optional
import uuid
from datetime import datetime
import logging

# Set up logger for user service
logger = logging.getLogger('auth')

class UserService:
    @staticmethod
    async def get_or_create_user_from_jwt_payload(session: Session, jwt_payload: dict) -> User:
        """
        Get existing user or create a new one based on JWT payload from Better Auth.
        Extracts user information from the JWT token's sub, email, and name claims.
        """
        try:
            # Extract user information from JWT payload
            user_id = jwt_payload.get('sub')
            email = jwt_payload.get('email')
            name = jwt_payload.get('name')

            if not user_id or not email:
                raise ValueError("JWT payload must contain 'sub' and 'email' claims")

            # Check if user already exists - user_id is a string
            statement = select(User).where(User.id == user_id)
            result = session.exec(statement)
            user = result.first()

            if user:
                # Update user info if needed (sync with JWT claims)
                update_needed = False
                if email != user.email:
                    user.email = email
                    update_needed = True
                if name != user.name:
                    user.name = name
                    update_needed = True

                if update_needed:
                    user.updated_at = datetime.utcnow()
                    session.add(user)
                    session.commit()
                    logger.info(f"Updated user info from JWT for user {user_id}")
                return user
            else:
                # Create new user from JWT payload
                user = User(
                    id=user_id,
                    email=email,
                    name=name
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                logger.info(f"Created new user from JWT: {user_id}")
                return user
        except Exception as e:
            logger.error(f"Error in get_or_create_user_from_jwt_payload: {e}")
            raise

    @staticmethod
    async def get_or_create_user(session: Session, user_id: str, email: str, name: Optional[str] = None) -> User:
        """
        Get existing user or create a new one based on Better Auth user info
        """
        try:
            # Check if user already exists
            statement = select(User).where(User.id == user_id)
            result = session.exec(statement)
            user = result.first()

            if user:
                # Update user info if needed
                update_needed = False
                if name and user.name != name:
                    user.name = name
                    update_needed = True
                if update_needed:
                    user.updated_at = datetime.utcnow()
                    session.add(user)
                    session.commit()
                    logger.info(f"Updated user info for user {user_id}")
                return user
            else:
                # Create new user
                user = User(
                    id=user_id,
                    email=email,
                    name=name
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                logger.info(f"Created new user {user_id}")
                return user
        except Exception as e:
            logger.error(f"Error in get_or_create_user: {e}")
            raise

    @staticmethod
    async def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """
        Get user by ID
        """
        try:
            statement = select(User).where(User.id == user_id)
            result = session.exec(statement)
            user = result.first()
            return user
        except Exception as e:
            logger.error(f"Error in get_user_by_id: {e}")
            raise

    @staticmethod
    async def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Get user by email
        """
        try:
            statement = select(User).where(User.email == email)
            result = session.exec(statement)
            user = result.first()
            return user
        except Exception as e:
            logger.error(f"Error in get_user_by_email: {e}")
            raise