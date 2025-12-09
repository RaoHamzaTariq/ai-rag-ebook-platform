# src/services/chunker_service.py
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkerService:
    """
    Split text into smaller chunks using LangChain text splitter
    """

    def __init__(self, chunk_size=800, chunk_overlap=100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def chunk_text(self, text):
        return self.splitter.split_text(text)
