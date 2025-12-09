# src/services/retriever.py
import asyncio

class Retriever:
    """
    Prioritized retriever for RAG system.
    """

    def __init__(self, qdrant_service):
        self.qdrant = qdrant_service

    async def retrieve(self, query_vector, current_page=None, highlighted_text=None, top_k=3):
        """
        Retrieve prioritized chunks from Qdrant.

        Priority order:
        1. Highlighted text matches
        2. Current page context
        3. Top global relevant chunks

        Args:
            query_vector: embedding vector for query
            current_page: optional page number
            highlighted_text: optional highlighted text
            top_k: number of chunks for each priority level
        """
        results = []

        # Priority 1: Highlighted text
        if highlighted_text:
            hl_vector = query_vector  # you can embed highlighted_text separately if needed
            hl_results = await self.qdrant.search(hl_vector, limit=top_k, score_threshold=0.7)
            results.extend(hl_results)

        # Priority 2: Current page
        if current_page is not None:
            page_results = await self.qdrant.client.query_points(
                collection_name=self.qdrant.collection_name,
                query=query_vector,
                limit=top_k,
                filter={"must": [{"key": "page_number", "match": {"value": current_page}}]},
                with_payload=True
            )
            results.extend(page_results.points)

        # Priority 3: Global top chunks
        global_results = await self.qdrant.search(query_vector, limit=top_k)
        results.extend(global_results)

        # Remove duplicates while preserving order
        seen_ids = set()
        prioritized_results = []
        for item in results:
            if item.id not in seen_ids:
                prioritized_results.append(item)
                seen_ids.add(item.id)

        return prioritized_results
