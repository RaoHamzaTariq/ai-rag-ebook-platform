# backend/src/agents/triage_agent.py
from agents import Agent
from src.agents.rag_agent import rag_agent  # noqa: ensure import path is correct


triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are the Triage Agent. Receive a user's query (and optional metadata like current_page or highlighted_text). 
    Decide if the query is simple and can be answered directly using your knowledge, 
    or if it requires retrieving content from the textbook. 
    If simple, answer directly; if not, hand off to the RAG Agent.
""",
    handoffs=[rag_agent],
    # Optionally you can set model_settings here if needed; else default is used
)
