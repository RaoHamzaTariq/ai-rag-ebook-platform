---
name: "rag-metadata-generator"
description: "Generate RAG metadata for each chapter of the 'Physical AI & Humanoid Robotics' textbook. Produces chapter_id, page_number, slug, title, url, and relevant content segments for ingestion by the RAG system."
version: "1.0.0"
---

# RAG Metadata Generator Skill

## When to Use This Skill

- User has finalized a chapter in MDX format and wants to prepare it for RAG ingestion
- User wants to automatically generate metadata for AI-based search and retrieval
- User wants to ensure all chapters follow a consistent structure for the RAG system

## How This Skill Works

1. **Read Chapter File**: Load MDX file from `content/chapters/`
2. **Extract Metadata**:
   - `chapter_id`
   - `page_number`
   - `slug`
   - `title`
   - `url`
3. **Segment Content**: Split chapter content into logical sections for RAG:
   - Introduction
   - Subtopics / Lessons
   - Examples
   - Code snippets
   - Diagrams / Figures
4. **Generate JSON Metadata Object** for the chapter:
   - Include extracted metadata
   - Include content segments with references to page numbers and headings
5. **Validate Metadata**:
   - Ensure chapter_id uniqueness
   - Check URL consistency
   - Verify all sections exist for ingestion
6. **Save Metadata**:
   - Output as `content/_data/rag-metadata.json`
   - Append or update existing entries for incremental chapter updates

## Output Format

Provide JSON with the following structure for each chapter:

```json
{
  "chapter_id": "01",
  "title": "Foundations of Physical AI & Embodied Intelligence",
  "slug": "foundations",
  "page_number": 1,
  "url": "/docs/01-foundations",
  "segments": [
    {
      "section_title": "Introduction",
      "text": "Introduction content..."
    },
    {
      "section_title": "Subtopic: Embodied Intelligence",
      "text": "Detailed content..."
    },
    {
      "section_title": "Examples",
      "text": "Example 1, Example 2..."
    }
  ]
}
````

### Example Input

* File: `content/chapters/01-foundations.mdx`

### Example Output

```json
{
  "chapter_id": "01",
  "title": "Foundations of Physical AI & Embodied Intelligence",
  "slug": "foundations",
  "page_number": 1,
  "url": "/docs/01-foundations",
  "segments": [
    {
      "section_title": "Introduction",
      "text": "Physical AI connects the digital brain with the physical world..."
    },
    {
      "section_title": "Examples",
      "text": "Example of robotic sensing using LIDAR and IMUs..."
    }
  ]
}
```
