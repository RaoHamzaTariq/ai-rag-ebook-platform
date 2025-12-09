# backend/src/agents/summarizer_agent.py
from agents import Agent

summarizer_agent = Agent(
    name="Summarizer Agent",
    instructions="""
You are the Summarizer Agent. Given a block of text (e.g. from a chapter or user-highlighted), 
produce a concise and clear summary. Preserve the meaning, maintain readability, 
and ensure the summary is significantly shorter than the original text while capturing main ideas.
""",
    # No handoffs: summarization is standalone.
)
