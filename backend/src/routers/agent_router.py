# backend/src/routers/agent_router.py
from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
from src.config.llm import config
from src.agents.triage_agent import triage_agent
from src.agents.summarizer_agent import summarizer_agent
from src.models.api_routes import AgentRequest
from src.models.context import UserContext
from agents import Runner

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/run")
async def run_agent(req: AgentRequest):

    user_context = UserContext(highlighted_text=req.highlighted_text,page_no=req.current_page)
    if req.agent_type.lower() == "triage":
        result = await Runner.run(triage_agent, req.query, context=user_context, run_config=config)
        return {"result": result.final_output}
    elif req.agent_type.lower() == "summarizer":
        result = await Runner.run(summarizer_agent, req.query, context=user_context, run_config=config)
        return {"summary": result.final_output}
    else:
        return {"error": "Unknown agent_type"}
