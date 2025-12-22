"""
Test suite for chat persistence functionality.
This includes tests for saving user messages, AI responses, and conversation history.
"""
import pytest
import asyncio
from datetime import datetime
from sqlmodel import Session, select
from unittest.mock import AsyncMock, Mock, patch

from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message
from src.services.user_service import UserService
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from src.config.database import engine


@pytest.mark.asyncio
async def test_user_creation_and_sync():
    """Test that users are properly created and synced from JWT data"""
    with Session(engine) as session:
        # Create a test user
        test_user_id = "test-user-123"
        test_email = "test@example.com"
        test_name = "Test User"

        user = await UserService.get_or_create_user(session, test_user_id, test_email, test_name)

        assert user.id == test_user_id
        assert user.email == test_email
        assert user.name == test_name

        # Test that getting the same user returns the same record
        same_user = await UserService.get_or_create_user(session, test_user_id, test_email, "Updated Name")
        assert same_user.id == test_user_id
        assert same_user.name == "Updated Name"  # Name should be updated

    print("✓ User creation and sync tests passed")


@pytest.mark.asyncio
async def test_conversation_creation():
    """Test that conversations are properly created and associated with users"""
    with Session(engine) as session:
        # First create a user
        test_user_id = "test-user-456"
        test_email = "test2@example.com"
        user = await UserService.get_or_create_user(session, test_user_id, test_email, "Test User 2")

        # Create a conversation for the user
        conversation_title = "Test Conversation"
        conversation = await ConversationService.create_conversation(session, test_user_id, conversation_title)

        assert conversation.user_id == user.id
        assert conversation.title == conversation_title
        assert conversation.is_active == True

    print("✓ Conversation creation tests passed")


@pytest.mark.asyncio
async def test_message_persistence():
    """Test that messages are properly saved and associated with conversations and users"""
    with Session(engine) as session:
        # Create a user
        test_user_id = "test-user-789"
        test_email = "test3@example.com"
        user = await UserService.get_or_create_user(session, test_user_id, test_email, "Test User 3")

        # Create a conversation
        conversation_title = "Test Conversation for Messages"
        conversation = await ConversationService.create_conversation(session, test_user_id, conversation_title)
        conversation_id = str(conversation.id)

        # Save a user message
        user_message_content = "Hello, this is a test message!"
        user_message = await MessageService.create_message(
            session=session,
            conversation_id=conversation_id,
            user_id=test_user_id,
            role="user",
            content=user_message_content
        )

        assert user_message.role == "user"
        assert user_message.content == user_message_content
        assert user_message.conversation_id == conversation.id
        assert user_message.user_id == user.id

        # Save an AI response
        ai_response_content = "Hello! This is an AI response to your message."
        sources = [{"slug": "handbook", "page_number": 1, "snippet": "test snippet"}]
        ai_message = await MessageService.create_message(
            session=session,
            conversation_id=conversation_id,
            user_id=test_user_id,
            role="assistant",
            content=ai_response_content,
            sources=sources,
            agent_type="rag"
        )

        assert ai_message.role == "assistant"
        assert ai_message.content == ai_response_content
        assert ai_message.sources == sources
        assert ai_message.agent_type == "rag"

    print("✓ Message persistence tests passed")


@pytest.mark.asyncio
async def test_conversation_history_retrieval():
    """Test that conversation history can be properly retrieved"""
    with Session(engine) as session:
        # Create a user
        test_user_id = "test-user-999"
        test_email = "test4@example.com"
        user = await UserService.get_or_create_user(session, test_user_id, test_email, "Test User 4")

        # Create a conversation
        conversation_title = "Test Conversation for History"
        conversation = await ConversationService.create_conversation(session, test_user_id, conversation_title)
        conversation_id = str(conversation.id)

        # Add multiple messages to the conversation
        messages = [
            ("user", "First message"),
            ("assistant", "First response"),
            ("user", "Second message"),
            ("assistant", "Second response")
        ]

        created_messages = []
        for role, content in messages:
            msg = await MessageService.create_message(
                session=session,
                conversation_id=conversation_id,
                user_id=test_user_id,
                role=role,
                content=content
            )
            created_messages.append(msg)

        # Retrieve all messages for the conversation
        retrieved_messages = await MessageService.get_conversation_messages(session, conversation_id, test_user_id)

        assert len(retrieved_messages) == len(created_messages)
        # Check that messages are returned in chronological order
        for i, retrieved_msg in enumerate(retrieved_messages):
            original_msg = created_messages[i]
            assert retrieved_msg.id == original_msg.id
            assert retrieved_msg.content == original_msg.content

        # Get user's conversations
        user_conversations = await ConversationService.get_user_conversations(session, test_user_id)
        assert len(user_conversations) >= 1
        assert any(conv.id == conversation.id for conv in user_conversations)

    print("✓ Conversation history retrieval tests passed")


@pytest.mark.asyncio
async def test_message_sources_storage():
    """Test that RAG sources are properly stored with messages"""
    with Session(engine) as session:
        # Create a user
        test_user_id = "test-user-sources"
        test_email = "sources@example.com"
        user = await UserService.get_or_create_user(session, test_user_id, test_email, "Sources Test User")

        # Create a conversation
        conversation = await ConversationService.create_conversation(session, test_user_id, "Test RAG Sources")
        conversation_id = str(conversation.id)

        # Create message with complex sources (typical RAG response)
        sources = [
            {
                "slug": "employee-handbook",
                "chapter_number": "3.2",
                "page_number": 45,
                "snippet": "All employees must follow the code of conduct outlined in section 3.2..."
            },
            {
                "slug": "company-policy",
                "chapter_number": "5.1",
                "page_number": 23,
                "snippet": "Remote work policy requires manager approval for more than 2 days per week..."
            }
        ]

        message_with_sources = await MessageService.create_message(
            session=session,
            conversation_id=conversation_id,
            user_id=test_user_id,
            role="assistant",
            content="Based on company policy, remote work requires manager approval for more than 2 days per week. Please refer to the employee handbook section 3.2 for code of conduct.",
            sources=sources
        )

        assert message_with_sources.sources is not None
        assert len(message_with_sources.sources) == 2
        assert message_with_sources.sources[0]["slug"] == "employee-handbook"
        assert message_with_sources.sources[1]["page_number"] == 23

        # Update sources for an existing message (useful for updating RAG sources after processing)
        updated_sources = [{"slug": "updated-doc", "page_number": 1, "snippet": "Updated information"}]
        updated_message = await MessageService.update_message_sources(session, str(message_with_sources.id), updated_sources)

        assert updated_message is not None
        assert len(updated_message.sources) == 1
        assert updated_message.sources[0]["slug"] == "updated-doc"

    print("✓ Message sources storage tests passed")


def run_chat_persistence_tests():
    """Run all chat persistence tests"""
    print("Running chat persistence tests...")

    # Run all async tests
    asyncio.run(test_user_creation_and_sync())
    asyncio.run(test_conversation_creation())
    asyncio.run(test_message_persistence())
    asyncio.run(test_conversation_history_retrieval())
    asyncio.run(test_message_sources_storage())

    print("All chat persistence tests completed successfully!")


if __name__ == "__main__":
    run_chat_persistence_tests()