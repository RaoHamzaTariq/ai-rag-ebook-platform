import os
import frontmatter
from typing import List, Dict

class MDXParser:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def scan_files(self) -> List[str]:
        mdx_files = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".mdx"):
                    mdx_files.append(os.path.join(root, file))
        return mdx_files

    def parse_file(self, file_path: str) -> Dict:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {}

        metadata = {
            "id": post.get("id", ""),
            "title": post.get("title", ""),
            "sidebar_label": post.get("sidebar_label", ""),
            "chapter_id": post.get("chapter_id", ""),
            "page_number": post.get("page_number", None),
            "slug": post.get("slug", ""),
            "source_file_path": file_path
        }

        content = post.content
        return {"metadata": metadata, "content": content}

    def parse_all_files(self) -> List[Dict]:
        results = []
        for file_path in self.scan_files():
            data = self.parse_file(file_path)
            if data:
                results.append(data)
        return results

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../frontend/docs"))
    parser = MDXParser(base_dir=BASE_DIR)
    all_data = parser.parse_all_files()
    print(f"Total MDX files parsed: {len(all_data)}")
    for item in all_data[:2]:
        print(item["metadata"])
        print(item["content"][:300], "...")
