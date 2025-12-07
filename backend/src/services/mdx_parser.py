# backend/src/services/mdx_parser.py

import os
import re
import yaml
from typing import List, Dict, Tuple


class MDXParserService:
    """
    Service to parse MDX files, extract frontmatter metadata and content.
    """

    def __init__(self, docs_root: str = "../../frontend/docs"):
        self.docs_root = os.path.abspath(docs_root)
        self.mdx_files: List[str] = []

    def scan_mdx_files(self) -> List[str]:
        """
        Recursively scan the docs directory for all .mdx files.
        """
        mdx_files = []
        for root, _, files in os.walk(self.docs_root):
            for file in files:
                if file.endswith(".mdx"):
                    mdx_files.append(os.path.join(root, file))
        self.mdx_files = mdx_files
        print(f"✅ Found {len(mdx_files)} MDX files")
        return mdx_files

    def parse_frontmatter(self, text: str) -> Tuple[Dict[str, str], str]:
        """
        Extract frontmatter metadata and content body from an MDX file.
        """
        frontmatter_pattern = re.compile(r"^---(.*?)---", re.DOTALL | re.MULTILINE)
        match = frontmatter_pattern.match(text)

        if match:
            frontmatter_block = match.group(1).strip()
            try:
                metadata = yaml.safe_load(frontmatter_block)
            except yaml.YAMLError as e:
                raise ValueError(f"Failed to parse YAML frontmatter: {e}")
            content = text[match.end():].strip()
        else:
            metadata = {}
            content = text

        return metadata, content

    def parse_mdx_file(self, file_path: str) -> Dict:
        """
        Parse a single MDX file and return metadata + content.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        metadata, content = self.parse_frontmatter(text)

        # Add file path to metadata for reference
        metadata["source_file_path"] = file_path

        return {
            "metadata": metadata,
            "content": content
        }

    def parse_all_files(self) -> List[Dict]:
        """
        Parse all MDX files and return a list of dicts with metadata and content.
        """
        if not self.mdx_files:
            self.scan_mdx_files()

        all_data = []
        for mdx_file in self.mdx_files:
            try:
                parsed = self.parse_mdx_file(mdx_file)
                all_data.append(parsed)
            except Exception as e:
                print(f"❌ Error parsing {mdx_file}: {e}")
        print(f"✅ Total MDX files parsed: {len(all_data)}")
        return all_data


# -----------------------------
# Test parser independently
# -----------------------------
if __name__ == "__main__":
    parser = MDXParserService(docs_root="../../frontend/docs")
    parser.scan_mdx_files()
    all_mdx_data = parser.parse_all_files()
    for item in all_mdx_data[:3]:  # print first 3 files for testing
        print("Metadata:", item["metadata"])
        print("Content snippet:", item["content"][:200], "\n")
