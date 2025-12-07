# backend/src/services/ingestion_pipeline.py
from mdx_parser import MDXParserService
from chunker_service import ChunkerService
from embedding_service import EmbeddingService
from qdrant_service import QdrantService


class IngestionPipeline:
    def __init__(self):
        self.parser = MDXParserService()
        self.chunker = ChunkerService()
        self.embedder = EmbeddingService()
        self.qdrant = QdrantService(collection_name="textbook_chunks")

    def ingest_all_files(self, docs_path: str):
        mdx_files = self.parser.scan_files(docs_path)
        total_chunks = 0

        for mdx_file in mdx_files:
            # Extract content and metadata
            content, metadata = self.parser.extract_content_metadata(mdx_file)

            # Chunk content
            chunks = self.chunker.create_chunks(content)

            # Embed chunks
            embeddings = self.embedder.embed_chunks(chunks)

            # Create repeated metadata for each chunk
            metadata_list = [metadata.copy() for _ in chunks]

            # Insert into Qdrant
            self.qdrant.insert_chunks(chunks, embeddings, metadata_list)

            total_chunks += len(chunks)

        print(f"✅ Total MDX files parsed: {len(mdx_files)}")
        print(f"✅ Total chunks inserted into Qdrant: {total_chunks}")

# Example usage
if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.ingest_all_files("..\\frontend\\docs")  # point to your docs folder
