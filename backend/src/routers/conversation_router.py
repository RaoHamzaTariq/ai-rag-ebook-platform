from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.api_routes import ConversationResponse, MessageResponse
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..dependencies.auth import get_current_user_id
from ..config.database import engine

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("/", response_model=List[ConversationResponse])
async def get_user_conversations(user_id: str = Depends(get_current_user_id)):
    """
    Get all conversations for the authenticated user.
    """
    try:
        with Session(engine) as session:
            conversations = await ConversationService.get_user_conversations(session, user_id)
            return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Get a specific conversation for the authenticated user.
    """
    try:
        with Session(engine) as session:
            conversation = await ConversationService.get_conversation_by_id(session, conversation_id, user_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            return conversation
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    limit: int = 50,
    offset: int = 0
):
    """
    Get all messages in a specific conversation for the authenticated user.
    """
    try:
        with Session(engine) as session:
            # Verify that the conversation belongs to the user
            conversation = await ConversationService.get_conversation_by_id(session, conversation_id, user_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")

            messages = await MessageService.get_conversation_messages(session, conversation_id, user_id, limit, offset)
            return messages
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def create_conversation_message(
    conversation_id: str,
    message_data: Message,
    user_id: str = Depends(get_current_user_id)
):
    """
    Create a new message in a conversation.
    """
    try:
        with Session(engine) as session:
            # Verify that the conversation belongs to the user
            conversation = await ConversationService.get_conversation_by_id(session, conversation_id, user_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")

            # Create the message
            message = await MessageService.create_message(
                session=session,
                conversation_id=conversation_id,
                user_id=user_id,
                role=message_data.role,
                content=message_data.content,
                sources=message_data.sources,
                agent_type=message_data.agent_type
            )
            return message
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation ID format or message data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")