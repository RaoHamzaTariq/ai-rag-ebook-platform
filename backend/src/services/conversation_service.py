from sqlmodel import Session, select
from ..models.conversation import Conversation
from ..models.user import User
from typing import List, Optional
import uuid
from datetime import datetime
import logging

# Set up logger for conversation service
logger = logging.getLogger('database')

class ConversationService:
    @staticmethod
    async def create_conversation(session: Session, user_id: str, title: str) -> Conversation:
        """
        Create a new conversation for a user
        """
        try:
            user_uuid = uuid.UUID(user_id)

            # Verify user exists
            user_statement = select(User).where(User.id == user_uuid)
            user_result = session.exec(user_statement)
            user = user_result.first()
            if not user:
                raise ValueError(f"User with ID {user_id} does not exist")

            conversation = Conversation(
                user_id=user_uuid,
                title=title
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            logger.info(f"Created conversation {conversation.id} for user {user_id}")
            return conversation
        except ValueError as e:
            logger.error(f"Error creating conversation: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in create_conversation: {e}")
            raise

    @staticmethod
    async def get_user_conversations(session: Session, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a user
        """
        try:
            user_uuid = uuid.UUID(user_id)
            statement = select(Conversation).where(
                Conversation.user_id == user_uuid,
                Conversation.is_active == True
            ).order_by(Conversation.updated_at.desc())
            result = session.exec(statement)
            conversations = result.all()
            logger.info(f"Retrieved {len(conversations)} conversations for user {user_id}")
            return conversations
        except ValueError as e:
            logger.error(f"Invalid UUID format for user_id {user_id}: {e}")
            raise ValueError(f"Invalid user ID format: {user_id}")
        except Exception as e:
            logger.error(f"Error in get_user_conversations: {e}")
            raise

    @staticmethod
    async def get_conversation_by_id(session: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for a user (ensures user owns the conversation)
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)

            statement = select(Conversation).where(
                Conversation.id == conv_uuid,
                Conversation.user_id == user_uuid,
                Conversation.is_active == True
            )
            result = session.exec(statement)
            conversation = result.first()

            if conversation:
                logger.info(f"Retrieved conversation {conversation_id} for user {user_id}")
            else:
                logger.info(f"Conversation {conversation_id} not found for user {user_id}")

            return conversation
        except ValueError as e:
            logger.error(f"Invalid UUID format - conversation_id: {conversation_id}, user_id: {user_id}: {e}")
            raise ValueError(f"Invalid ID format")
        except Exception as e:
            logger.error(f"Error in get_conversation_by_id: {e}")
            raise

    @staticmethod
    async def update_conversation(session: Session, conversation_id: str, user_id: str, title: Optional[str] = None) -> Optional[Conversation]:
        """
        Update a conversation's details
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)

            # Get the conversation to update
            statement = select(Conversation).where(
                Conversation.id == conv_uuid,
                Conversation.user_id == user_uuid,
                Conversation.is_active == True
            )
            result = session.exec(statement)
            conversation = result.first()

            if not conversation:
                logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
                return None

            # Update fields if provided
            if title is not None:
                conversation.title = title
            conversation.updated_at = datetime.utcnow()

            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            logger.info(f"Updated conversation {conversation_id}")
            return conversation
        except ValueError as e:
            logger.error(f"Invalid UUID format: {e}")
            raise ValueError(f"Invalid ID format")
        except Exception as e:
            logger.error(f"Error in update_conversation: {e}")
            raise

    @staticmethod
    async def delete_conversation(session: Session, conversation_id: str, user_id: str) -> bool:
        """
        Soft delete a conversation by setting is_active to False
        """
        try:
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)

            statement = select(Conversation).where(
                Conversation.id == conv_uuid,
                Conversation.user_id == user_uuid,
                Conversation.is_active == True
            )
            result = session.exec(statement)
            conversation = result.first()

            if not conversation:
                logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
                return False

            conversation.is_active = False
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            logger.info(f"Soft deleted conversation {conversation_id}")
            return True
        except ValueError as e:
            logger.error(f"Invalid UUID format: {e}")
            raise ValueError(f"Invalid ID format")
        except Exception as e:
            logger.error(f"Error in delete_conversation: {e}")
            raise