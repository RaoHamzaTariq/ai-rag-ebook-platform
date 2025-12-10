"""
Retrieve-only script – no inserts, just query the existing vectors.
"""
from __future__ import annotations

import asyncio
from typing import List, Any

from qdrant_client import models


class Retriever:
    def __init__(self, qdrant_service) -> None:
        self.qdrant = qdrant_service

    async def retrieve(
        self,
        query: str | list[float],
        current_page: int | None = None,
        highlighted_text: str | None = None,
        top_k: int = 8,  # Increased default from 5 to 8
        score_threshold: float = 0.65,  # Lowered from 0.70 to be more inclusive
    ) -> List[Any]:
        from src.services.embedding_service import EmbeddingService
        embed = EmbeddingService().embed

        results: List[Any] = []

        # 1. Prioritize highlighted text with higher weight
        if highlighted_text:
            highlighted_results = await self.qdrant.search(
                highlighted_text, 
                limit=top_k, 
                score_threshold=max(0.60, score_threshold - 0.05)  # Slightly lower threshold for highlighted text
            )
            # Boost scores for highlighted text results
            for point in highlighted_results:
                point.score = min(1.0, point.score * 1.1)  # 10% boost
            results.extend(highlighted_results)

        # 2. Current page context (if available)
        if current_page is not None:
            vector = query if isinstance(query, list) else embed(query, isSingle=True)
            page_results = (
                await self.qdrant.client.query_points(
                    collection_name=self.qdrant.collection_name,
                    query=vector,
                    query_filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="page_number",
                                match=models.MatchValue(value=str(current_page)),
                            )
                        ]
                    ),
                    limit=top_k,
                    with_payload=True,
                    with_vectors=False,
                )
            ).points
            # Boost scores for current page results
            for point in page_results:
                point.score = min(1.0, point.score * 1.05)  # 5% boost
            results.extend(page_results)

        # 3. Global semantic search (always perform for comprehensive results)
        if isinstance(query, str):
            global_results = await self.qdrant.search(
                query, 
                limit=top_k * 2,  # Get more results for better coverage
                score_threshold=score_threshold
            )
            results.extend(global_results)
        else:
            global_results = (
                await self.qdrant.client.query_points(
                    collection_name=self.qdrant.collection_name,
                    query=query,
                    limit=top_k * 2,
                    with_payload=True,
                    with_vectors=False,
                )
            ).points
            results.extend(global_results)

        # Smart deduplication: keep highest score for each unique chunk
        seen = {}
        for p in results:
            chunk_id = str(p.id)
            if chunk_id not in seen or p.score > seen[chunk_id].score:
                seen[chunk_id] = p
        
        # Sort by score (highest first) and return top_k results
        out = sorted(seen.values(), key=lambda x: x.score, reverse=True)[:top_k]
        return out


async def _main() -> None:
    from src.services.qdrant_service import QdrantService

    print("Connecting to live Qdrant …")
    qdrant = QdrantService(collection_name="retriever_test", vector_size=768)

    # create index once (uncomment next 3 lines on first run, then comment out again)
    # await qdrant.client.create_payload_index(
    #     collection_name="physical_ai_chunks",
    #     field_name="page_number",
    #     field_schema=models.PayloadSchemaType.INTEGER,
    # )

    retriever = Retriever(qdrant)
    hits = await retriever.retrieve(
        query="neural nets",
        current_page=5,  # remove this if you do not have the index yet
        highlighted_text="machine learning",
        top_k=5,
    )

    print(f"\nRetriever returned {len(hits)} unique chunks:")
    for h in hits:
        print(f"  score={h.score:.3f}  page={h.payload.get('page_number')}  text={h.payload.get('text')[:120]}...")

    await qdrant.close()
    print("\n✅ retrieve-only test finished.")


if __name__ == "__main__":
    asyncio.run(_main())