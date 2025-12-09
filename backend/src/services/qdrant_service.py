import os
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QdrantService:

    def __init__(self, collection_name="physical_ai_chunks", vector_size=768):
        # Get env variables with validation
        qdrant_url = os.environ.get("QDRANT_ENDPOINT")
        qdrant_key = os.environ.get("QDRANT_API_KEY")
        
        if not qdrant_url or not qdrant_key:
            raise ValueError("QDRANT_ENDPOINT and QDRANT_API_KEY must be set in environment")
        
        # Ensure URL has proper format (add :6333 port if not present)
        if ":6333" not in qdrant_url and not qdrant_url.endswith(":443"):
            qdrant_url = f"{qdrant_url}:6333"
        
        print(f"[QDRANT] Connecting to: {qdrant_url}")
        
        self.client = AsyncQdrantClient(
            url=qdrant_url,
            api_key=qdrant_key,
            timeout=30
        )
        self.collection_name = collection_name
        self.vector_size = vector_size

    async def _ensure_collection(self):
        try:
            exists = await self.client.collection_exists(self.collection_name)
            if exists:
                print(f"[QDRANT] Collection '{self.collection_name}' already exists.")
                return

            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"[QDRANT] Collection '{self.collection_name}' created successfully.")
        except Exception as e:
            print(f"[QDRANT ERROR] Failed to ensure collection: {e}")
            raise

    async def upload(self, chunks, embeddings, metadata_list):
        """
        Upload chunks with embeddings to Qdrant
        
        Args:
            chunks: List of text chunks
            embeddings: List of embedding vectors
            metadata_list: List of metadata dicts (one per chunk)
        """
        await self._ensure_collection()

        # Validate inputs
        if not (len(chunks) == len(embeddings) == len(metadata_list)):
            raise ValueError("chunks, embeddings, and metadata_list must have same length")

        # Get existing collection info to determine next available ID
        collection_info = await self.client.get_collection(self.collection_name)
        start_id = collection_info.points_count  # Start from current count
        
        points = []
        for i, (chunk, emb, meta) in enumerate(zip(chunks, embeddings, metadata_list)):
            # Validate embedding dimension
            if len(emb) != self.vector_size:
                raise ValueError(f"Embedding dimension {len(emb)} doesn't match vector_size {self.vector_size}")
            
            # Use unique incremental ID starting from existing count
            unique_id = start_id + i
            
            points.append(PointStruct(
                id=unique_id,
                vector=emb,
                payload={"text": chunk, **meta}
            ))

        try:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True,
            )
            print(f"[QDRANT] Successfully uploaded {len(points)} chunks (IDs: {start_id} to {start_id + len(points) - 1})")
        except Exception as e:
            print(f"[QDRANT ERROR] Upload failed: {e}")
            raise

    async def search(self, query_vector, limit=5, score_threshold=0.7):
        """Search for similar vectors using query_points (AsyncQdrantClient method)"""
        try:
            if len(query_vector) != self.vector_size:
                raise ValueError(
                    f"Query embedding must be {self.vector_size}-dimensional, got {len(query_vector)}"
                )

            # Use query_points for AsyncQdrantClient (NOT search)
            search_results = await self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True
            )
            
            # Return the points from the result
            return search_results.points
        
        except Exception as e:
            print(f"[QDRANT ERROR] Search failed: {e}")
            raise

    async def close(self):
        """Close the client connection"""
        await self.client.close()


async def test_connection():
    """Test Qdrant connection and basic operations"""
    try:
        # Initialize with smaller vector size for testing
        qdrant = QdrantService(collection_name="test_collection", vector_size=3)
        
        # Test data - note metadata_list is now a LIST of dicts
        chunks = ["Hi How are you"]
        embeddings = [[0.343, -0.42, 0.53]]
        metadata_list = [{"id": 23, "source": "test"}]
        
        # Test upload
        print("\n=== Testing Upload ===")
        await qdrant.upload(chunks, embeddings, metadata_list)
        
        # Test search
        print("\n=== Testing Search ===")
        results = await qdrant.search(embeddings[0], limit=1, score_threshold=0.0)
        
        if results:
            for result in results:
                print(f"Score: {result.score:.4f}, Text: {result.payload.get('text')}")
        else:
            print("No results found")
        
        # Cleanup
        await qdrant.close()
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_connection())