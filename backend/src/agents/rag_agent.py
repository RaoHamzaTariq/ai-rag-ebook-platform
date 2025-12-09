# backend/src/agents/rag_agent.py
from agents import Agent, Tool, Runner, RunContextWrapper, function_tool, ModelSettings
from src.services.retriever import Retriever  # your retriever service
# from src.models.context import UserContext
from src.models.api_routes import AgentRequest
from src.services.qdrant_service import QdrantService
import asyncio 

# Initialize your retriever (already implemented in Phase 7)
retriever = Retriever(qdrant_service=QdrantService())

@function_tool(name_override="retrieve_data")
async def retrieve_chunks(query: str, current_page: int | None = None, highlighted_text: str | None = None):
    """
    Calls the retriever to get relevant chunks based on the query and optional context.
    Args:
        query:str
        current_page: int | None = None
        highlighted_text: str | None = None 

    Returns a formatted string combining all chunks.
    """
    chunks = await retriever.retrieve(
        query=query,
        current_page=current_page,
        highlighted_text=highlighted_text
    )
    # Combine text chunks into a single context string
    return "\n\n".join([chunk["text"] for chunk in chunks])

async def dynamic_instructions(
    context: RunContextWrapper[AgentRequest],
    agent: Agent[AgentRequest]
) -> str:
    current_page = context.context.page_no
    highlighted_text = context.context.highlighted_text
    query= context.context.query

    extracted_text = await retrieve_chunks(query,current_page, highlighted_text)

    return f"""
    You are the RAG Agent. So please provide proper answer

    Current Page: {current_page}
    highlighted_text: {highlighted_text}

    Extracted Text: {extracted_text}
    """


rag_agent = Agent[AgentRequest](
    name="RAG Agent",
    instructions=dynamic_instructions,
    # tools=[retrieve_chunks],
    # model_settings=ModelSettings(tool_choice="required")
)
