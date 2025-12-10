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
        highlighted_text=highlighted_text,
        top_k=8,  # Increased from 5 to get more context
        score_threshold=0.65  # Slightly lowered to be more inclusive
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
    serialized_chunks = []
    formatted_texts = []
    
    # Sort points by score (highest first) for better context
    sorted_points = sorted(points, key=lambda p: p.score, reverse=True)
    
    for idx, point in enumerate(sorted_points, 1):
        payload = point.payload or {}
        text = payload.get("text", "")
        page = payload.get("page_number", "unknown")
        chapter = payload.get("chapter_number", "unknown")
        
        # Format with metadata for better context
        formatted_chunk = f"[Source {idx} - Chapter {chapter}, Page {page}, Relevance: {point.score:.2f}]\n{text}"
        formatted_texts.append(formatted_chunk)
        
        # Add to retrieved_chunks with metadata
        serialized_chunks.append({
            "text": text,
            "page_number": payload.get("page_number"),
            "slug": payload.get("slug", ""), 
            "chapter_number": payload.get("chapter_number", ""),
            "score": point.score
        })

    context.context.retrieved_chunks = serialized_chunks

    extracted_text = "\n\n".join(formatted_texts)
    
    # Build context-aware prompt
    context_info = []
    if highlighted_text:
        context_info.append(f"User selected text: '{highlighted_text[:200]}...'")
    if current_page:
        context_info.append(f"User is viewing page: {current_page}")
    
    context_section = "\n".join(context_info) if context_info else "No additional context provided."
    
    num_sources = len(formatted_texts)
    
    return f"""You are an expert Physical AI textbook assistant. Your role is to provide accurate, helpful answers based on the retrieved textbook content.

**User Context:**
{context_section}

**User Question:**
{query}

**Retrieved Content ({num_sources} relevant sources):**
{extracted_text}

**Instructions:**
1. **Analyze the retrieved sources carefully** - They are ranked by relevance (highest first)
2. **Synthesize information** from multiple sources when applicable
3. **Answer the user's question directly and comprehensively**
4. **Use clear, educational language** appropriate for a textbook assistant
5. **If the sources contain the answer:**
   - Provide a complete, well-structured response
   - Cite which sources you used (e.g., "According to Source 1...")
   - Include relevant examples or details from the sources
   - Explain concepts clearly, building on the textbook content

6. **If the sources don't fully answer the question:**
   - Provide what information IS available from the sources
   - Be honest about what's not covered
   - Suggest related topics the user might explore

7. **Format your response:**
   - Start with a direct answer
   - Provide supporting details and explanations
   - Use bullet points or numbered lists for clarity when appropriate
   - Keep paragraphs concise and readable

**Important:**
- Base your answer PRIMARILY on the retrieved sources
- Don't make up information not present in the sources
- If sources conflict, acknowledge different perspectives
- Be helpful, accurate, and educational

Now, answer the user's question using the retrieved content above.
"""


rag_agent = Agent[AgentRequest](
    name="RAG Agent",
    instructions=dynamic_instructions,
    # tools=[retrieve_chunks],
    # model_settings=ModelSettings(tool_choice="required")
)
