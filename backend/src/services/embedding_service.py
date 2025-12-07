# backend/src/services/embedding_service.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class EmbeddingService:
    def __init__(self):
        # Initialize Gemini embeddings model
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def embed_chunks(self, chunks: list):
        """
        Generate embeddings for each text chunk
        """
        return [self.embedding_model.embed_query(chunk) for chunk in chunks]

# Example usage
if __name__ == "__main__":
    chunks = ["Hello world", "Second chunk"]
    emb_service = EmbeddingService()
    vectors = emb_service.embed_chunks(chunks)
    print(vectors)
