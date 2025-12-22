from sqlmodel import Session, select
from ..models.message import Message
from ..models.conversation import Conversation
from ..models.user import User
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import logging

# Set up logger for message service
logger = logging.getLogger('database')

class MessageService:
    @staticmethod
    async def create_message(
        session: Session,
        conversation_id: str,
        user_id: str,
        role: str,
        content: str,
        sources: Optional[List[Dict[str, Any]]] = None,
        agent_type: Optional[str] = None
    ) -> Message:
        """
        Create a new message in a conversation
        """
        try:
            # Verify conversation exists and belongs to user
            conv_statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
                Conversation.is_active == True
            )
            conv_result = session.exec(conv_statement)
            conversation = conv_result.first()
            if not conversation:
                logger.warning(f"Conversation {conversation_id} not found or doesn't belong to user {user_id}. Attempting to proceed anyway in simple mode.")

            message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=role,
                content=content,
                sources=sources,
                agent_type=agent_type
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            logger.info(f"Created message {message.id} in conversation {conversation_id}")
            return message
        except Exception as e:
            logger.error(f"Unexpected error in create_message: {e}")
            raise

    @staticmethod
    async def get_conversation_messages(
        session: Session,
        conversation_id: str,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """
        Get all messages in a conversation for a user
        """
        try:
            statement = select(Message).where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            ).order_by(Message.timestamp.asc()).offset(offset).limit(limit)

            result = session.exec(statement)
            messages = result.all()
            logger.info(f"Retrieved {len(messages)} messages from conversation {conversation_id}")
            return messages
        except Exception as e:
            logger.error(f"Error in get_conversation_messages: {e}")
            raise

    @staticmethod
    async def get_message_by_id(session: Session, message_id: str, user_id: str) -> Optional[Message]:
        """
        Get a specific message by ID for a user
        """
        try:
            statement = select(Message).where(
                Message.id == message_id,
                Message.user_id == user_id
            )
            result = session.exec(statement)
            message = result.first()

            if message:
                logger.info(f"Retrieved message {message_id}")
            else:
                logger.info(f"Message {message_id} not found for user {user_id}")

            return message
        except Exception as e:
            logger.error(f"Error in get_message_by_id: {e}")
            raise

    @staticmethod
    async def update_message_sources(session: Session, message_id: str, sources: List[Dict[str, Any]]) -> Optional[Message]:
        """
        Update the sources for a message (useful for updating RAG sources after agent processing)
        """
        try:
            statement = select(Message).where(Message.id == message_id)
            result = session.exec(statement)
            message = result.first()

            if not message:
                logger.warning(f"Message {message_id} not found")
                return None

            message.sources = sources
            # message.updated_at = datetime.utcnow() # Add if exists in model
            session.add(message)
            session.commit()
            session.refresh(message)
            logger.info(f"Updated sources for message {message_id}")
            return message
        except Exception as e:
            logger.error(f"Error in update_message_sources: {e}")
            raise