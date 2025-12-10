# # src/services/retriever.py
# import asyncio

# from qdrant_client.models import Filter, FieldCondition, MatchValue


# class Retriever:
#     """
#     Prioritized retriever for RAG system.
#     """

#     def __init__(self, qdrant_service):
#         self.qdrant = qdrant_service

#     async def retrieve(self, query, current_page=None, highlighted_text=None, top_k=3):
#         """
#         Retrieve prioritized chunks from Qdrant.

#         Priority order:
#         1. Highlighted text matches
#         2. Current page context
#         3. Top global relevant chunks

#         Args:
#             query: query string or embedding vector
#             current_page: optional page number
#             highlighted_text: optional highlighted text
#             top_k: number of chunks for each priority level
#         """
#         from src.services.embedding_service import EmbeddingService
        
#         results = []

#         # Priority 1: Highlighted text
#         if highlighted_text:
#             # For highlighted text, we search using the highlighted text itself as the query
#             # This implementation assumes qdrant.search handles embedding
#             hl_results = await self.qdrant.search(highlighted_text, limit=top_k, score_threshold=0.7)
#             results.extend(hl_results)

#         # Prepare query vector if needed
#         query_vector = None
#         if isinstance(query, str):
#             # We need the vector for direct client queries (Priority 2)
#             if current_page is not None:
#                 embedding_service = EmbeddingService()
#                 query_vector = embedding_service.embed(query, isSingle=True)
#         else:
#             query_vector = query

#         # Priority 2: Current page
#         if current_page is not None:
#             # We need a vector for query_points with filter
#             if query_vector is None:
#                  # Should not happen if query is vector, but if query is str and we failed to embed...
#                  # But we embedded above.
#                  pass

#             page_results = await self.qdrant.client.query_points(
#                 collection_name=self.qdrant.collection_name,
#                 query=query_vector,
#                 limit=top_k,
#                 query_filter=Filter(
#                     must=[
#                         FieldCondition(
#                             key="page_number",
#                             match=MatchValue(value=current_page)
#                         )
#                     ]
#                 ),
#                 with_payload=True
#             )

#             results.extend(page_results.points)

#         # Priority 3: Global top chunks
#         if isinstance(query, str):
#             global_results = await self.qdrant.search(query, limit=top_k)
#         else:
#             # If query is already a vector, use query_points directly
#             global_results_obj = await self.qdrant.client.query_points(
#                 collection_name=self.qdrant.collection_name,
#                 query=query,
#                 limit=top_k,
#                 with_payload=True
#             )
#             global_results = global_results_obj.points
            
#         results.extend(global_results)

#         # Remove duplicates while preserving order
#         seen_ids = set()
#         prioritized_results = []
#         for item in results:
#             if item.id not in seen_ids:
#                 prioritized_results.append(item)
#                 seen_ids.add(item.id)

#         return prioritized_results




"""
Prioritised retriever for RAG system.
1. highlighted-text matches
2. current-page context
3. global best chunks
"""
from __future__ import annotations

import asyncio
from typing import List

from qdrant_client import models


# ------------------------------------------------------------------
# Retriever
# ------------------------------------------------------------------
class Retriever:
    def __init__(self, qdrant_service) -> None:
        self.qdrant = qdrant_service

    async def retrieve(
        self,
        query: str | List[float],
        current_page: int | None = None,
        highlighted_text: str | None = None,
        top_k: int = 3,
        score_threshold: float = 0.70,
    ) -> List[models.ScoredPoint]:
        """
        Return de-duplicated ScoredPoint list in priority order.
        """
        from src.services.embedding_service import EmbeddingService  # local import avoids circular deps
        embed = EmbeddingService().embed

        results: List[models.ScoredPoint] = []

        # ---------- 1. highlighted text ----------
        if highlighted_text:
            hl_results = await self.qdrant.search(
                highlighted_text,
                limit=top_k,
                score_threshold=score_threshold,
            )
            results.extend(hl_results)

        # ---------- 2. current page ----------
        if current_page is not None:
            vector = query if isinstance(query, list) else embed(query, isSingle=True)
            page_res = await self.qdrant.client.query_points(
                collection_name=self.qdrant.collection_name,
                query=vector,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="page_number",
                            match=models.MatchValue(value=current_page),
                        )
                    ]
                ),
                limit=top_k,
                with_payload=True,
                with_vectors=False,
            )
            results.extend(
                models.ScoredPoint(id=p.id, score=p.score or 0.0, payload=p.payload or {})
                for p in page_res.points
            )

        # ---------- 3. global ----------
        if isinstance(query, str):
            global_results = await self.qdrant.search(query, limit=top_k)
        else:
            global_res = await self.qdrant.client.query_points(
                collection_name=self.qdrant.collection_name,
                query=query,
                limit=top_k,
                with_payload=True,
                with_vectors=False,
            )
            global_results = [
                models.ScoredPoint(id=p.id, score=p.score or 0.0, payload=p.payload or {})
                for p in global_res.points
            ]
        results.extend(global_results)

        # ---------- de-duplicate ----------
        seen, out = set(), []
        for item in results:
            key = str(item.id)
            if key not in seen:
                seen.add(key)
                out.append(item)
        return out


# ------------------------------------------------------------------
# quick CLI test
# ------------------------------------------------------------------
async def _main() -> None:
    from src.services.qdrant_service import QdrantService
    from src.services.embedding_service import EmbeddingService

    print("Connecting to live Qdrant …")
    qdrant = QdrantService(collection_name="retriever_test", vector_size=768)
    await qdrant._ensure_collection()

    # ---- tiny test data ----
    chunks = [
        "This chunk lives on page 5 and talks about machine learning.",
        "Another chunk on page 5 discussing neural nets.",
        "Page 99 contains completely unrelated text.",
    ]
    # emb_service = EmbeddingService()
    # embeddings = emb_service.embed(chunks)  # sync
    # meta = [
    #     {"page_number": 5, "source": "test"},
    #     {"page_number": 5, "source": "test"},
    #     {"page_number": 99, "source": "test"},
    # ]

    # upload
    # print("Uploading 3 test chunks …")
    # await qdrant.upload(chunks, embeddings, meta)

    # retrieve
    retriever = Retriever(qdrant)
    hits = await retriever.retrieve(
        query="neural nets",
        current_page=5,
        highlighted_text="machine learning",
        top_k=5,
    )

    print(f"\nRetriever returned {len(hits)} unique chunks:")
    for h in hits:
        print(f"  score={h.score:.3f}  page={h.payload.get('page_number')}  text={h.payload.get('text')}")

    await qdrant.close()
    print("\n✅ retriever.py smoke test finished.")


if __name__ == "__main__":
    asyncio.run(_main())