# src/services/mdx_parser_service.py
import os
import re
from pathlib import Path

class MDXParserService:
    """
    Parse .mdx files and extract text chunks with metadata
    """

    def __init__(self, docs_root="../frontend/docs"):
        self.docs_root = Path(docs_root)

    def get_mdx_files(self):
        return list(self.docs_root.rglob("*.mdx"))

    def parse_file(self, file_path):
        """
        Parses frontmatter and content from a .mdx file.
        Returns: dict with metadata and full content string
        """
        content = file_path.read_text(encoding="utf-8")
        # Extract YAML frontmatter
        frontmatter_match = re.match(r"---(.*?)---", content, re.S)
        metadata = {}
        if frontmatter_match:
            fm_lines = frontmatter_match.group(1).splitlines()
            for line in fm_lines:
                if ":" in line:
                    key, val = line.split(":", 1)
                    metadata[key.strip()] = val.strip()
        # Remove frontmatter
        content_without_fm = re.sub(r"---(.*?)---", "", content, flags=re.S).strip()
        return {"metadata": metadata, "content": content_without_fm}

if __name__ == "__main__":
    parser = MDXParserService()

    # Get all MDX files
    mdx_files = parser.get_mdx_files()
    print(f"Found {len(mdx_files)} .mdx file(s).")

    # Parse each file and print metadata and first 200 characters of content
    for file_path in mdx_files:
        print(f"\nParsing file: {file_path}")
        result = parser.parse_file(file_path)
        print("Metadata:", result["metadata"])
        print("Content preview:", result["content"][:200], "...\n")

    