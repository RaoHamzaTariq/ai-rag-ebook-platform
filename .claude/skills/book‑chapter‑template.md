---
name: "book-chapter-template"
description: "Generate well-structured chapters for the 'Physical AI & Humanoid Robotics' textbook. Ensures MDX formatting, metadata, headings, code blocks, diagrams, personalization, and translation placeholders. Use whenever a new chapter needs to be authored."
version: "1.0.0"
---

# Book Chapter Template Skill

## When to Use This Skill

- User wants to create a new chapter for the textbook
- User needs standardized MDX formatting with proper metadata
- User wants placeholders for code snippets, diagrams, personalization, or translation

## How This Skill Works

1. **Add Metadata**: Insert YAML frontmatter including chapter_id, page_number, slug, title, URL
2. **Structure Headings**: Create main headings and subheadings for chapter sections
3. **Insert Content Sections**:
   - Explanations
   - Examples / Analogies
   - Code snippets (Python / ROS 2)
   - Diagrams / Illustrations
4. **Personalization & Translation**:
   - Insert `{personalization_placeholder}` if personalization_flag is true
   - Insert `{translation_placeholder}` if translation_flag is true
5. **Finalize MDX**: Ensure the chapter is ready for Docusaurus ingestion and RAG system

## Output Format

Provide a fully formatted MDX chapter with:

- YAML frontmatter:
  - `chapter_id`
  - `page_number`
  - `slug`
  - `title`
  - `url`
- Headings and subheadings for all subtopics
- Placeholder blocks for code snippets and diagrams
- Optional personalization and translation placeholders

### Example Output (MDX)

```mdx
---
chapter_id: 01
page_number: 1
slug: foundations-of-physical-ai
title: Foundations of Physical AI & Embodied Intelligence
url: /chapters/01-foundations
---

# Foundations of Physical AI & Embodied Intelligence

## Learning Objectives
- Understand Physical AI principles and embodied intelligence
- Learn the importance of embodied AI in humanoid robotics
- Apply foundational knowledge to humanoid simulations

## 1. Introduction
Content goes here…

## 2. Subtopic 1
Explanation content goes here…

### Example
Example content goes here…

### Code Snippet
```python
# Placeholder for Python / ROS 2 code snippet
````

### Diagram

![Diagram Description](../assets/chapters/01-foundations/diagram1.png)

## 3. Subtopic 2

Content goes here…

<!-- Personalization Placeholder -->

{personalization_placeholder}

<!-- Translation Placeholder -->

{translation_placeholder}

```

## Example Input

- chapter_number: 1  
- chapter_title: "Foundations of Physical AI & Embodied Intelligence"  
- learning_objectives: ["Understand Physical AI", "Learn humanoid robotics basics"]  
- subtopics: ["Introduction", "History of Physical AI", "Applications"]  
- code_snippets: []  
- diagrams: []  
- personalization_flag: true  
- translation_flag: true

## Example Output

A fully structured MDX file as shown in **Example Output (MDX)** section.