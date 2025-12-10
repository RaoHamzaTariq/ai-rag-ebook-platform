from fastapi import APIRouter
from src.config.llm import config
from src.agents.triage_agent import triage_agent
from src.agents.summarizer_agent import summarizer_agent
from src.models.api_routes import AgentRequest, AgentResponse
from src.utils.logging_config import logger, log_agent_decision, log_error
from agents import Runner
from typing import Optional
import uuid

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/run", response_model=AgentResponse)
async def run_agent(req: AgentRequest):
    """
    Run an agent based on the request type.
    Supports triage, summarizer, and (future) RAG agents.
    """
    session_id = req.session_id or str(uuid.uuid4())

    try:
        # Log the incoming request
        logger.info(
            f"Agent request received - Session: {session_id}, "
            f"Type: {req.agent_type}, Query: {req.query[:50]}..."
        )

        # Determine which agent to run
        agent_type_lower = req.agent_type.lower()
        if agent_type_lower == "triage":
            result = await Runner.run(triage_agent, req.query, context=req, run_config=config)
            response = AgentResponse(
                message=result.final_output,
                agent_used="triage"
            )
        elif agent_type_lower == "summarizer":
            result = await Runner.run(summarizer_agent, req.query, context=req, run_config=config)
            response = AgentResponse(
                message=result.final_output,
                agent_used="summarizer"
            )
        elif agent_type_lower == "rag":
            # Placeholder for future RAG implementation
            response = AgentResponse(
                message="RAG agent is not yet implemented",
                agent_used="rag"
            )
        else:
            error_msg = f"Unknown agent_type: {req.agent_type}"
            log_error(error_msg, session_id)
            response = AgentResponse(
                message=f"Unknown agent_type: {req.agent_type}. Supported types: triage, summarizer, rag",
                agent_used="unknown"
            )

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

        return AgentResponse(
            message="An error occurred while processing your request. Please try again.",
            agent_used="error"
        )
