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
            # Verify user exists
            user_statement = select(User).where(User.id == user_id)
            user_result = session.exec(user_statement)
            user = user_result.first()
            
            if not user:
                logger.error(f"Failed to create conversation: User with ID {user_id} does not exist in the database.")
                raise ValueError(f"User with ID {user_id} not found. A user must exist before creating a conversation.")

            conversation = Conversation(
                user_id=user_id,
                title=title
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            logger.info(f"Created conversation {conversation.id} for user {user_id}")
            return conversation
        except Exception as e:
            logger.error(f"Unexpected error in create_conversation: {e}")
            raise

    @staticmethod
    async def get_user_conversations(session: Session, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a user
        """
        try:
            statement = select(Conversation).where(
                Conversation.user_id == user_id,
                Conversation.is_active == True
            ).order_by(Conversation.updated_at.desc())
            result = session.exec(statement)
            conversations = result.all()
            logger.info(f"Retrieved {len(conversations)} conversations for user {user_id}")
            return conversations
        except Exception as e:
            logger.error(f"Error in get_user_conversations: {e}")
            raise

    @staticmethod
    async def get_conversation_by_id(session: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for a user (ensures user owns the conversation)
        """
        try:
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
                Conversation.is_active == True
            )
            result = session.exec(statement)
            conversation = result.first()

            if conversation:
                logger.info(f"Retrieved conversation {conversation_id} for user {user_id}")
            else:
                logger.info(f"Conversation {conversation_id} not found for user {user_id}")

            return conversation
        except Exception as e:
            logger.error(f"Error in get_conversation_by_id: {e}")
            raise

    @staticmethod
    async def update_conversation(session: Session, conversation_id: str, user_id: str, title: Optional[str] = None) -> Optional[Conversation]:
        """
        Update a conversation's details
        """
        try:
            # Get the conversation to update
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
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
        except Exception as e:
            logger.error(f"Error in update_conversation: {e}")
            raise

    @staticmethod
    async def delete_conversation(session: Session, conversation_id: str, user_id: str) -> bool:
        """
        Soft delete a conversation by setting is_active to False
        """
        try:
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
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
        except Exception as e:
            logger.error(f"Error in delete_conversation: {e}")
            raise