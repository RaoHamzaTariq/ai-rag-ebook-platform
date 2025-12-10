# src/services/retriever.py
import asyncio

from qdrant_client.models import Filter, FieldCondition, MatchValue


class Retriever:
    """
    Prioritized retriever for RAG system.
    """

    def __init__(self, qdrant_service):
        self.qdrant = qdrant_service

    async def retrieve(self, query, current_page=None, highlighted_text=None, top_k=3):
        """
        Retrieve prioritized chunks from Qdrant.

        Priority order:
        1. Highlighted text matches
        2. Current page context
        3. Top global relevant chunks

        Args:
            query: query string or embedding vector
            current_page: optional page number
            highlighted_text: optional highlighted text
            top_k: number of chunks for each priority level
        """
        from src.services.embedding_service import EmbeddingService
        
        results = []

        # Priority 1: Highlighted text
        if highlighted_text:
            # For highlighted text, we search using the highlighted text itself as the query
            # This implementation assumes qdrant.search handles embedding
            hl_results = await self.qdrant.search(highlighted_text, limit=top_k, score_threshold=0.7)
            results.extend(hl_results)

        # Prepare query vector if needed
        query_vector = None
        if isinstance(query, str):
            # We need the vector for direct client queries (Priority 2)
            if current_page is not None:
                embedding_service = EmbeddingService()
                query_vector = embedding_service.embed(query, isSingle=True)
        else:
            query_vector = query

        # Priority 2: Current page
        if current_page is not None:
            # We need a vector for query_points with filter
            if query_vector is None:
                 # Should not happen if query is vector, but if query is str and we failed to embed...
                 # But we embedded above.
                 pass

            page_results = await self.qdrant.client.query_points(
                collection_name=self.qdrant.collection_name,
                query=query_vector,
                limit=top_k,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="page_number",
                            match=MatchValue(value=current_page)
                        )
                    ]
                ),
                with_payload=True
            )

            results.extend(page_results.points)

        # Priority 3: Global top chunks
        if isinstance(query, str):
            global_results = await self.qdrant.search(query, limit=top_k)
        else:
            # If query is already a vector, use query_points directly
            global_results_obj = await self.qdrant.client.query_points(
                collection_name=self.qdrant.collection_name,
                query=query,
                limit=top_k,
                with_payload=True
            )
            global_results = global_results_obj.points
            
        results.extend(global_results)

        # Remove duplicates while preserving order
        seen_ids = set()
        prioritized_results = []
        for item in results:
            if item.id not in seen_ids:
                prioritized_results.append(item)
                seen_ids.add(item.id)

        return prioritized_results
