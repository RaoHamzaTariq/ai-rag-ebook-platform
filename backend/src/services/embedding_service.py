# src/services/embedding_service.py

import os
import requests
from time import sleep

class EmbeddingService:
    """
    Service to generate embeddings for text chunks using
    Google Gemini embeddings API with batching and rate limiting.
    """

    def __init__(self, model="text-embedding-004", batch_size=5, retry=5, base_wait_seconds=2):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY must be set in environment variables")
        
        # Use text-embedding-004 for better stability
        self.model = model
        self.batch_size = batch_size
        self.retry = retry
        self.base_wait_seconds = base_wait_seconds
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:batchEmbedContents"

    def _chunk_batches(self, chunks):
        """Yield successive batches of chunks"""
        for i in range(0, len(chunks), self.batch_size):
            yield chunks[i:i + self.batch_size]

    def embed(self, chunks):
        """Generate embeddings for all chunks in batches with exponential backoff"""
        all_embeddings = []
        total_batches = (len(chunks) + self.batch_size - 1) // self.batch_size
        batch_num = 0

        for batch in self._chunk_batches(chunks):
            batch_num += 1
            print(f"[EmbeddingService] Processing batch {batch_num}/{total_batches} ({len(batch)} chunks)")
            
            payload = {"requests": []}
            for text in batch:
                payload["requests"].append({
                    "model": f"models/{self.model}",
                    "content": {"parts": [{"text": text}]}
                })

            # Retry logic with exponential backoff
            for attempt in range(self.retry):
                try:
                    response = requests.post(
                        self.url,
                        headers={
                            "x-goog-api-key": self.api_key,
                            "Content-Type": "application/json"
                        },
                        json=payload,
                        timeout=60
                    )
                    response.raise_for_status()
                    data = response.json()

                    # Extract embeddings
                    for item in data["embeddings"]:
                        all_embeddings.append(item["values"])
                    
                    print(f"[EmbeddingService] ✓ Batch {batch_num}/{total_batches} completed")
                    
                    # Add delay between successful batches to avoid rate limits
                    if batch_num < total_batches:
                        sleep(1)  # 1 second between batches
                    
                    break  # success, break retry loop

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:  # Too Many Requests
                        # Exponential backoff: 2s, 4s, 8s, 16s, 32s
                        wait_time = self.base_wait_seconds * (2 ** attempt)
                        print(f"[EmbeddingService] ⚠ Rate limit hit. Waiting {wait_time}s before retry {attempt+1}/{self.retry}")
                        sleep(wait_time)
                        
                        if attempt == self.retry - 1:
                            print(f"[EmbeddingService] ✗ Failed after {self.retry} attempts")
                            raise e
                    else:
                        print(f"[EmbeddingService] HTTP Error: {e}")
                        raise e
                        
                except requests.exceptions.RequestException as e:
                    print(f"[EmbeddingService] Network error on attempt {attempt+1}: {e}")
                    if attempt < self.retry - 1:
                        wait_time = self.base_wait_seconds * (2 ** attempt)
                        sleep(wait_time)
                    else:
                        raise e

        print(f"[EmbeddingService] ✓ All {len(all_embeddings)} embeddings generated successfully")
        return all_embeddings


# Alternative: Ultra-slow mode for strict rate limits
class SlowEmbeddingService(EmbeddingService):
    """
    Ultra-conservative embedding service for free tier API limits.
    Processes 1 chunk at a time with delays.
    """
    
    def __init__(self, model="text-embedding-004", delay_per_request=2):
        super().__init__(model=model, batch_size=1, retry=5, base_wait_seconds=5)
        self.delay_per_request = delay_per_request
    
    def embed(self, chunks):
        """Generate embeddings one at a time with delays"""
        print(f"[SlowEmbeddingService] Processing {len(chunks)} chunks (1 at a time with {self.delay_per_request}s delay)")
        all_embeddings = []
        
        for i, chunk in enumerate(chunks, 1):
            if i % 10 == 0 or i == 1:  # Print progress every 10 chunks
                print(f"[SlowEmbeddingService] Processing chunk {i}/{len(chunks)}")
            
            # Use parent's embed method with single chunk
            embedding = super().embed([chunk])
            all_embeddings.extend(embedding)
            
            # Delay between requests
            if i < len(chunks):
                sleep(self.delay_per_request)
        
        print(f"[SlowEmbeddingService] ✓ Completed all {len(chunks)} chunks")
        return all_embeddings