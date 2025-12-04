---
name: "mdx-format-validator"
description: "Validate MDX chapter files for the 'Physical AI & Humanoid Robotics' textbook. Ensures correct YAML frontmatter, headings, subheadings, code blocks, diagram links, personalization and translation placeholders. Use before RAG ingestion or deployment."
version: "1.0.0"
---

# MDX Format Validator Skill

## When to Use This Skill

- User wants to check a chapter before adding it to the book repository
- User needs to ensure MDX compatibility with Docusaurus
- User wants to verify that chapter contains all required metadata, headings, and placeholders
- User wants to prevent RAG ingestion errors due to formatting issues

## How This Skill Works

1. **Check YAML Frontmatter**: Verify presence of:
   - `chapter_id`
   - `page_number`
   - `slug`
   - `title`
   - `url`
2. **Validate Headings & Subheadings**:
   - Check that all major sections (Introduction, Subtopics, Examples, Code Snippets, Diagrams) exist
   - Ensure proper Markdown heading levels (`#`, `##`, `###`)
3. **Check Code Snippets & Diagram Links**:
   - Validate that all code blocks have language tags (e.g., ```python)
   - Ensure diagram links point to existing files in `assets` folder
4. **Personalization & Translation Placeholders**:
   - Confirm presence if `personalization_flag` or `translation_flag` is true
5. **Report Errors**:
   - Missing or malformed metadata
   - Incorrect heading levels
   - Missing placeholders
   - Invalid diagram paths

## Output Format

Provide:

- **Validation Status**: Passed / Failed
- **Errors / Warnings**: List of issues detected
- **Suggestions**: How to fix each issue

### Example Input

- Path: `content/chapters/01-foundations.mdx`  
- Personalization_flag: true  
- Translation_flag: true  

### Example Output

```json
{
  "validation_status": "Failed",
  "errors": [
    "Missing frontmatter: page_number",
    "Diagram ../assets/chapters/01-foundations/diagram1.png not found",
    "Heading 'Learning Objectives' missing"
  ],
  "suggestions": [
    "Add page_number in YAML frontmatter",
    "Add or correct diagram file path",
    "Include 'Learning Objectives' heading with proper content"
  ]
}
