from fastapi import APIRouter, Depends
from src.config.llm import config
from src.agents.triage_agent import triage_agent
from src.agents.summarizer_agent import summarizer_agent
from src.agents.rag_agent import rag_agent
from src.models.api_routes import AgentRequest, AgentResponse
from src.utils.logging_config import logger, log_agent_decision, log_error
from src.dependencies.auth import get_current_user_id
from agents import Runner
from typing import Optional
import uuid
from src.services.message_service import MessageService
from src.services.conversation_service import ConversationService
from sqlmodel import Session
from src.config.database import engine


router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/run", response_model=AgentResponse)
async def run_agent(req: AgentRequest, user_id: str = Depends(get_current_user_id)):
    """
    Run an agent based on the request type.
    Supports triage, summarizer, and RAG agents.
    Requires authentication.
    """
    session_id = req.session_id or str(uuid.uuid4())

    try:
        # Log the incoming request with user ID
        logger.info(
            f"Agent request received - User: {user_id}, Session: {session_id}, "
            f"Type: {req.agent_type}, Query: {req.query[:50]}..."
        )

        # Get or create conversation
        with Session(engine) as session:
            # Check if conversation exists, create if not
            conversation = await ConversationService.get_conversation_by_id(session, session_id, user_id)
            if not conversation:
                # Create a new conversation with a title based on the first query
                title = req.query[:50] + "..." if len(req.query) > 50 else req.query
                conversation = await ConversationService.create_conversation(session, user_id, title)
                session_id = str(conversation.id)

            # Save user message to database
            user_message = await MessageService.create_message(
                session=session,
                conversation_id=session_id,
                user_id=user_id,
                role="user",
                content=req.query,
                agent_type=req.agent_type
            )
            logger.info(f"Saved user message to database: {user_message.id}")

        # Determine which agent to run
        agent_type_lower = req.agent_type.lower()
        if agent_type_lower == "triage":
            result = await Runner.run(triage_agent, req.query, context=req, run_config=config)
            response = AgentResponse(
                message=result.final_output,
                agent_used="triage" # It might have handed off, but we started with triage. Ideally we check result.agent.name
            )
        elif agent_type_lower == "summarizer":
            result = await Runner.run(summarizer_agent, req.query, context=req, run_config=config)
            response = AgentResponse(
                message=result.final_output,
                agent_used="summarizer"
            )
        elif agent_type_lower == "rag":
            result = await Runner.run(rag_agent, req.query, context=req, run_config=config)
            response = AgentResponse(
                message=result.final_output,
                agent_used="rag"
            )
        else:
            error_msg = f"Unknown agent_type: {req.agent_type}"
            log_error(error_msg, session_id)
            response = AgentResponse(
                message=f"Unknown agent_type: {req.agent_type}. Supported types: triage, summarizer, rag",
                agent_used="unknown"
            )

        # Populate sources if RAG retrieved anything
        sources = []
        if req.retrieved_chunks:
            for chunk in req.retrieved_chunks:
                sources.append({
                    "slug": chunk.get("slug", "handbook"), # Default slug if missing
                    "chapter_number": str(chunk.get("chapter_number", "")),
                    "page_number": int(chunk.get("page_number") or 0),
                    "snippet": chunk.get("text", "")[:150] + "..."
                })
            response.sources = sources

        # Save agent response to database
        with Session(engine) as session:
            agent_message = await MessageService.create_message(
                session=session,
                conversation_id=session_id,
                user_id=user_id,  # For agent messages, we'll use the same user_id as the owner of the conversation
                role="assistant",
                content=response.message,
                sources=sources if sources else None,
                agent_type=response.agent_used
            )
            logger.info(f"Saved agent response to database: {agent_message.id}")

        # Log the agent decision
        log_agent_decision(
            session_id=session_id,
            query=req.query,
            agent_type=req.agent_type,
            decision=response.agent_used
        )

        return response

    except Exception as e:
        error_msg = f"Error processing agent request: {str(e)}"
        log_error(error_msg, session_id)
        logger.error(error_msg, exc_info=True)

        # Even in case of error, we should save the error response as an assistant message
        try:
            with Session(engine) as session:
                # Try to save error message to database as well
                error_response = AgentResponse(
                    message="An error occurred while processing your request. Please try again.",
                    agent_used="error"
                )
                error_message = await MessageService.create_message(
                    session=session,
                    conversation_id=session_id,
                    user_id=user_id,
                    role="assistant",
                    content=error_response.message,
                    agent_type=error_response.agent_used
                )
                logger.info(f"Saved error response to database: {error_message.id}")
        except Exception as db_error:
            logger.error(f"Failed to save error response to database: {db_error}")

        return AgentResponse(
            message="An error occurred while processing your request. Please try again.",
            agent_used="error"
        )
