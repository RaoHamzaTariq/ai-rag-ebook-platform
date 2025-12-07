# backend/src/services/chunker_service.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ChunkerService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Uses LangChain RecursiveCharacterTextSplitter
        chunk_size: max tokens per chunk
        chunk_overlap: tokens overlap between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def create_chunks(self, content: str):
        """
        Splits content into chunks
        """
        return self.text_splitter.split_text(content)

# Example usage
if __name__ == "__main__":
    content = "Your MDX content here..."
    chunker = ChunkerService()
    chunks = chunker.create_chunks(content)
    print(f"Total Chunks: {len(chunks)}")
