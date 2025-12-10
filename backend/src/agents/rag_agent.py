# backend/src/agents/rag_agent.py
from agents import Agent, Tool, Runner, RunContextWrapper, function_tool, ModelSettings
from src.services.retriever import Retriever  # your retriever service
# from src.models.context import UserContext
from src.models.api_routes import AgentRequest
from src.services.qdrant_service import QdrantService
import asyncio 

# Initialize your retriever (already implemented in Phase 7)
retriever = Retriever(qdrant_service=QdrantService())

# @function_tool(name_override="retrieve_data")
async def retrieve_data(query: str, current_page: int | None = None, highlighted_text: str | None = None):
    """
    Calls the retriever to get relevant chunks based on the query and optional context.
    Returns the raw points.
    """
    return await retriever.retrieve(
        query=query,
        current_page=current_page,
        highlighted_text=highlighted_text
    )

async def dynamic_instructions(
    context: RunContextWrapper[AgentRequest],
    agent: Agent[AgentRequest]
) -> str:
    current_page = context.context.current_page
    highlighted_text = context.context.highlighted_text
    query = context.context.query

    # Retrieve points (chunks)
    page_num = int(current_page) if current_page and current_page.isdigit() else None
    points = await retrieve_data(query, page_num, highlighted_text)
    
    # Store in context for the router to pick up
    # We convert PointStruct to dict for easier serialization or processing later
    # Point object usually has .payload
    serialized_chunks = []
    formatted_texts = []
    
    for point in points:
        payload = point.payload or {}
        text = payload.get("text", "")
        formatted_texts.append(text)
        
        # Add to retrieved_chunks with metadata
        serialized_chunks.append({
            "text": text,
            "page_number": payload.get("page_number"),
            "slug": payload.get("slug", ""), # Assuming slug might be there or not
            "chapter_number": payload.get("chapter_number", ""),
            "score": point.score
        })

    context.context.retrieved_chunks = serialized_chunks

    extracted_text = "\n\n".join(formatted_texts)

    return f"""
    You are the RAG Agent. Using the following retrieved context from the textbook, verify and answer the user's question.
    Only use the provided context. If the answer is not in the context, say so.
    
    Current Page: {current_page}
    highlighted_text: {highlighted_text}

    Extracted Text: 
    {extracted_text}
    """


rag_agent = Agent[AgentRequest](
    name="RAG Agent",
    instructions=dynamic_instructions,
    # tools=[retrieve_chunks],
    # model_settings=ModelSettings(tool_choice="required")
)
