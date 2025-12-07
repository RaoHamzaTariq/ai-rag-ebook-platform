import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from dotenv import load_dotenv

load_dotenv()


class QdrantService:
    """
    Service class to manage Qdrant connection, collections, and vector insertion.
    """

    def __init__(self, collection_name: str = "textbook_chunks", vector_size: int = None):
        self.endpoint = os.environ.get("QDRANT_ENDPOINT")
        self.api_key = os.environ.get("QDRANT_API_KEY")
        self.client: QdrantClient = None

        self.collection_name = collection_name
        self.vector_size = vector_size or int(os.environ.get("VECTOR_SIZE", 1536))

        self._validate_env()
        self.connect()
        self.create_collection()

    def _validate_env(self):
        if not self.endpoint or not self.api_key:
            raise RuntimeError("QDRANT_ENDPOINT and QDRANT_API_KEY must be set in .env")

    def connect(self):
        """Connects to the Qdrant database."""
        try:
            self.client = QdrantClient(
                url=self.endpoint,
                api_key=self.api_key
            )
            print("✅ Connected to Qdrant")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Qdrant: {e}")

    def create_collection(self):
        """Creates the collection if it does not exist."""
        if self.client.collection_exists(collection_name=self.collection_name):
            print(f"Collection '{self.collection_name}' already exists ✅")
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{self.collection_name}' created ✅")

    def insert_chunks(self, chunks: List[str], embeddings: List[List[float]], metadata_list: List[Dict[str, Any]]):
        """
        Inserts a list of chunks with embeddings and metadata into the Qdrant collection.

        Args:
            chunks (List[str]): List of text chunks.
            embeddings (List[List[float]]): Corresponding vector embeddings.
            metadata_list (List[Dict[str, Any]]): List of metadata dicts (slug, chapter_number, etc.)

        Raises:
            ValueError: If lengths of chunks, embeddings, and metadata_list do not match.
        """
        if not (len(chunks) == len(embeddings) == len(metadata_list)):
            raise ValueError("Lengths of chunks, embeddings, and metadata_list must match.")

        points = []
        for i in range(len(chunks)):
            points.append(
                PointStruct(
                    id=i,  # optional, Qdrant can generate if omitted
                    vector=embeddings[i],
                    payload={
                        "text": chunks[i],
                        **metadata_list[i]
                    }
                )
            )

        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"✅ Inserted {len(points)} chunks into '{self.collection_name}'")
        except Exception as e:
            print(f"❌ Error inserting chunks: {e}")



