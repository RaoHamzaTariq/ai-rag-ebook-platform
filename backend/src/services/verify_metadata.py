# src/services/verify_metadata.py

import asyncio
from src.services.qdrant_service import QdrantService
from src.services.embedding_service import EmbeddingService

async def verify_metadata():
    """Verify that metadata is properly stored in Qdrant"""
    
    print("\n" + "="*60)
    print("🔍 VERIFYING QDRANT METADATA")
    print("="*60 + "\n")
    
    # Initialize services
    qdrant = QdrantService(collection_name="physical_ai_chunks", vector_size=768)
    embedder = EmbeddingService(batch_size=1)
    
    try:
        # Get collection info
        collection_info = await qdrant.client.get_collection("physical_ai_chunks")
        print(f"📊 Collection Stats:")
        print(f"   - Total points: {collection_info.points_count}")
        print(f"   - Vector size: {collection_info.config.params.vectors.size}")
        print(f"   - Distance: {collection_info.config.params.vectors.distance}")
        print()
        
        # Test search with a sample query
        test_query = "What is embodied intelligence?"
        print(f"🔎 Testing search with query: '{test_query}'")
        
        # Generate embedding for test query
        query_embedding = embedder.embed([test_query])[0]
        
        # Search
        results = await qdrant.search(
            query_vector=query_embedding,
            limit=5,
            score_threshold=0.0  # Get all results
        )
        
        print(f"\n✅ Found {len(results)} results\n")
        
        # Display results with metadata
        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  Score: {result.score:.4f}")
            print(f"  ID: {result.id}")
            print(f"  Metadata:")
            for key, value in result.payload.items():
                if key != "text":  # Don't print the full text
                    print(f"    - {key}: {value}")
            # Print first 100 chars of text
            text = result.payload.get("text", "")
            print(f"  Text preview: {text[:100]}...")
            print()
        
        # Get a random sample of points
        print("\n" + "="*60)
        print("📋 SAMPLE METADATA FROM COLLECTION")
        print("="*60 + "\n")
        
        # Scroll through first 10 points
        scroll_result = await qdrant.client.scroll(
            collection_name="physical_ai_chunks",
            limit=10,
            with_payload=True,
            with_vectors=False
        )
        
        points, next_offset = scroll_result
        
        for point in points:
            print(f"Point ID: {point.id}")
            print(f"Metadata fields: {list(point.payload.keys())}")
            metadata = {k: v for k, v in point.payload.items() if k != "text"}
            for key, value in metadata.items():
                print(f"  - {key}: {value}")
            print()
        
        await qdrant.close()
        
        print("\n" + "="*60)
        print("✅ VERIFICATION COMPLETE")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        await qdrant.close()


if __name__ == "__main__":
    asyncio.run(verify_metadata())