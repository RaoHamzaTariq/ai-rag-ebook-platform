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
        top_k: int = 5,
        score_threshold: float = 0.70,
    ) -> List[Any]:
        from src.services.embedding_service import EmbeddingService
        embed = EmbeddingService().embed

        results: List[Any] = []

        # 1. highlighted text
        if highlighted_text:
            results.extend(
                await self.qdrant.search(highlighted_text, limit=top_k, score_threshold=score_threshold)
            )

        # 2. current page (only if index exists)
        if current_page is not None:
            vector = query if isinstance(query, list) else embed(query, isSingle=True)
            results.extend(
                (
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
            )

        # 3. global
        if isinstance(query, str):
            results.extend(await self.qdrant.search(query, limit=top_k))
        else:
            results.extend(
                (
                    await self.qdrant.client.query_points(
                        collection_name=self.qdrant.collection_name,
                        query=query,
                        limit=top_k,
                        with_payload=True,
                        with_vectors=False,
                    )
                ).points
            )

        # de-duplicate
        seen, out = set(), []
        for p in results:
            if str(p.id) not in seen:
                seen.add(str(p.id))
                out.append(p)
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