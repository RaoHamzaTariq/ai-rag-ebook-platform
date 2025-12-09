# src/services/ingestion_pipeline.py

import os
import asyncio
import sys
from pathlib import Path
from src.services.qdrant_service import QdrantService
from src.services.embedding_service import EmbeddingService, SlowEmbeddingService
from langchain_text_splitters import RecursiveCharacterTextSplitter

class IngestionPipeline:
    def __init__(self, docs_path="../frontend/docs", use_slow_mode=False):
        self.docs_path = Path(docs_path)
        self.chunk_size = 800          # characters per chunk
        self.chunk_overlap = 100        # overlap between chunks
        
        # Choose embedding service based on mode
        if use_slow_mode:
            print("[Pipeline] 🐢 SLOW MODE: Processing 1 chunk at a time with 2s delay")
            print("[Pipeline] This will take ~6 minutes for 177 chunks but avoids rate limits")
            self.embedder = SlowEmbeddingService(delay_per_request=2)
        else:
            print("[Pipeline] ⚡ BATCH MODE: Processing 5 chunks per batch with exponential backoff")
            self.embedder = EmbeddingService(batch_size=5, retry=5, base_wait_seconds=2)
        
        self.qdrant = QdrantService(collection_name="physical_ai_chunks", vector_size=768)

    def _extract_frontmatter(self, text):
        """Extract YAML frontmatter from MDX file"""
        import re
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
        if not frontmatter_match:
            return {}
        
        metadata = {}
        fm_content = frontmatter_match.group(1)
        for line in fm_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"').strip("'")
        return metadata
    
    def _extract_chapter(self, file_path):
        """Extract chapter from path like '01-foundations' -> 'Foundations'"""
        parts = file_path.parts
        for part in parts:
            if '-' in part and part[0].isdigit():
                return part.split('-', 1)[1].replace('-', ' ').title()
        return "Unknown"
    
    def _extract_section(self, file_path):
        """Extract section from filename like '1-1-embodied-intelligence.mdx'"""
        name = file_path.stem  # Get filename without extension
        if '-' in name:
            # Split on dash and capitalize
            parts = name.split('-')
            # Remove numeric prefixes
            section_parts = [p for p in parts if not p.replace('.', '').isdigit()]
            return ' '.join(section_parts).title()
        return name.title()

    async def run(self):
        all_chunks = []
        metadata_list = []

        # Walk through all MDX files
        mdx_files = list(self.docs_path.rglob("*.mdx"))
        print(f"[Pipeline] Found {len(mdx_files)} MDX files")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        for mdx_file in mdx_files:
            text = mdx_file.read_text(encoding="utf-8")
            
            # Extract frontmatter metadata if exists
            frontmatter_meta = self._extract_frontmatter(text)
            
            chunks = splitter.split_text(text)
            all_chunks.extend(chunks)
            
            # Create rich metadata per chunk
            relative_path = mdx_file.relative_to(self.docs_path)
            for chunk_idx, chunk in enumerate(chunks):
                metadata = {
                    "file_path": str(relative_path),
                    "filename": mdx_file.name,
                    "chapter": self._extract_chapter(mdx_file),
                    "section": self._extract_section(mdx_file),
                    "chunk_index": chunk_idx,
                    "total_chunks": len(chunks),
                    **frontmatter_meta  # Add any frontmatter metadata
                }
                metadata_list.append(metadata)

            print(f"[OK] {relative_path} → {len(chunks)} chunks")

        if not all_chunks:
            print("[Pipeline] No chunks to process!")
            return

        # Generate embeddings
        print(f"[Pipeline] Generating embeddings for {len(all_chunks)} chunks...")
        try:
            embeddings = self.embedder.embed(all_chunks)
        except Exception as e:
            print(f"\n[Pipeline ERROR] Embedding failed: {e}")
            print("\n💡 SOLUTIONS:")
            print("1. Wait 1 minute and try again (quota may reset)")
            print("2. Use slow mode: python -m src.services.ingestion_pipeline --slow")
            print("3. Reduce batch_size further in embedding_service.py")
            print("4. Check your Google API quota at: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas")
            raise

        # Upload to Qdrant
        print(f"[Pipeline] Uploading {len(embeddings)} vectors to Qdrant...")
        await self.qdrant.upload(all_chunks, embeddings, metadata_list)
        await self.qdrant.close()
        print("\n" + "="*60)
        print("✅ INGESTION COMPLETED SUCCESSFULLY!")
        print(f"📊 Total chunks processed: {len(all_chunks)}")
        print(f"📦 Vectors uploaded to Qdrant: {len(embeddings)}")
        print("="*60)


if __name__ == "__main__":
    # Check for --slow flag
    use_slow = "--slow" in sys.argv
    
    if use_slow:
        print("\n" + "="*60)
        print("🐢 SLOW MODE ENABLED")
        print("This will take longer but is more reliable for free tier")
        print("Estimated time: ~6 minutes for 177 chunks")
        print("="*60 + "\n")
    
    pipeline = IngestionPipeline(use_slow_mode=use_slow)
    asyncio.run(pipeline.run())