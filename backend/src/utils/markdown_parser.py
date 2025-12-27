import re
import os
from typing import List, Dict, Any
from pathlib import Path


def extract_title_from_markdown(content: str, file_path: str) -> str:
    """
    Extract the title from markdown content or filename.
    """
    # Try to find the first H1 header
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()

    # If no H1 found, try H2
    h2_match = re.search(r'^##\s+(.+)$', content, re.MULTILINE)
    if h2_match:
        return h2_match.group(1).strip()

    # If no headers found, use the filename
    return Path(file_path).stem.replace('-', ' ').replace('_', ' ').title()


def parse_markdown_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a markdown file and extract its content and metadata.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title_from_markdown(content, file_path)

    return {
        'title': title,
        'content': content,
        'path': file_path,
        'word_count': len(content.split()),
        'char_count': len(content)
    }


def get_all_markdown_files(docs_directory: str) -> List[str]:
    """
    Recursively find all markdown files in the docs directory.
    """
    markdown_files = []
    docs_path = Path(docs_directory)

    if not docs_path.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_directory}")

    # Look for .md and .mdx files
    for ext in ['.md', '.mdx']:
        markdown_files.extend(list(docs_path.rglob(f"*{ext}")))

    # Convert to string paths
    return [str(file_path) for file_path in markdown_files]


def extract_frontmatter(content: str) -> tuple:
    """
    Extract frontmatter from markdown content if present.
    Returns (frontmatter_dict, content_without_frontmatter)
    """
    if content.startswith('---'):
        # Find the end of frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            import yaml
            try:
                frontmatter = yaml.safe_load(parts[1])
                content_without_frontmatter = parts[2]
                return frontmatter or {}, content_without_frontmatter
            except yaml.YAMLError:
                # If YAML parsing fails, return empty frontmatter
                return {}, content

    return {}, content


def get_section_type(content: str) -> str:
    """
    Determine the section type based on content characteristics.
    """
    content_lower = content.lower()

    # Check for code blocks
    if '```' in content:
        return 'code_section'

    # Check for configuration or setup
    setup_indicators = ['install', 'setup', 'configure', 'configuration', 'environment', 'requirements']
    if any(indicator in content_lower for indicator in setup_indicators):
        return 'setup_section'

    # Check for concepts or theory
    concept_indicators = ['concept', 'theory', 'overview', 'introduction', 'what is', 'definition']
    if any(indicator in content_lower for indicator in concept_indicators):
        return 'conceptual_section'

    # Check for tutorials or guides
    guide_indicators = ['how to', 'tutorial', 'guide', 'step', 'example', 'implement']
    if any(indicator in content_lower for indicator in guide_indicators):
        return 'tutorial_section'

    # Default
    return 'content_section'


def parse_markdown_with_sections(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse markdown file and split into sections preserving document structure.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter if present
    frontmatter, content = extract_frontmatter(content)

    # Extract title
    title = extract_title_from_markdown(content, file_path)

    # Split content by headers to maintain document structure
    sections = []
    header_pattern = r'(\n|^)(#{1,6})\s+(.+?)(?=\n|$)'
    header_matches = list(re.finditer(header_pattern, content))

    if not header_matches:
        # No headers, return the whole content as one section
        section_type = get_section_type(content)
        sections.append({
            'title': title,
            'content': content,
            'type': section_type,
            'path': file_path,
            'word_count': len(content.split()),
            'frontmatter': frontmatter
        })
    else:
        # Process content with headers
        start = 0
        for match in header_matches:
            # Add content before this header as a section
            header_start = match.start()
            if header_start > start:
                section_content = content[start:header_start].strip()
                if section_content:
                    sections.append({
                        'title': title,
                        'content': section_content,
                        'type': get_section_type(section_content),
                        'path': file_path,
                        'word_count': len(section_content.split()),
                        'frontmatter': frontmatter
                    })

            # Move start to after this header
            start = match.end()

        # Add any remaining content after the last header
        if start < len(content):
            remaining_content = content[start:].strip()
            if remaining_content:
                sections.append({
                    'title': title,
                    'content': remaining_content,
                    'type': get_section_type(remaining_content),
                    'path': file_path,
                    'word_count': len(remaining_content.split()),
                    'frontmatter': frontmatter
                })

        # Add the top-level content if any exists before the first header
        if header_matches and header_matches[0].start() > 0:
            before_first_header = content[:header_matches[0].start()].strip()
            if before_first_header:
                sections.insert(0, {
                    'title': title,
                    'content': before_first_header,
                    'type': get_section_type(before_first_header),
                    'path': file_path,
                    'word_count': len(before_first_header.split()),
                    'frontmatter': frontmatter
                })

    # If no sections were created, add the whole content as one section
    if not sections:
        sections.append({
            'title': title,
            'content': content,
            'type': get_section_type(content),
            'path': file_path,
            'word_count': len(content.split()),
            'frontmatter': frontmatter
        })

    return sections