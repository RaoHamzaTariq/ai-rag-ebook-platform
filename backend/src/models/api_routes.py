from pydantic import BaseModel
class AgentRequest(BaseModel):
    agent_type: str  # "triage" or "summarizer"
    query: str
    current_page: int | None = None
    highlighted_text: str | None = None
    # For summarizer agent maybe the field name is 'text' — but we use 'query' for simplicity