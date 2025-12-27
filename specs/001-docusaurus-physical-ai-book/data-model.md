# Data Model: Physical AI & Humanoid Robotics Book

## Entities

### Course Module
- **id**: string (unique identifier for the module)
- **title**: string (display title of the module)
- **description**: string (brief description of the module content)
- **order**: number (sequence in which modules appear)
- **pages**: array of Page objects (content pages in the module)
- **learningObjectives**: array of strings (learning objectives for the module)
- **prerequisites**: array of strings (required knowledge before starting)
- **duration**: string (estimated time to complete)

### Page
- **id**: string (unique identifier for the page)
- **title**: string (display title of the page)
- **content**: string (Markdown/MDX content)
- **module**: string (reference to parent module id)
- **order**: number (sequence within the module)
- **type**: string (content type: text, code, diagram, exercise, etc.)
- **learningObjectives**: array of strings (objectives for this page)
- **relatedPages**: array of strings (IDs of related pages)

### Interactive Element
- **id**: string (unique identifier for the element)
- **type**: string (code-block, diagram, simulation, etc.)
- **content**: string or object (the actual content or configuration)
- **page**: string (reference to parent page id)
- **position**: number (order within the page)

### Code Example
- **id**: string (unique identifier for the code example)
- **language**: string (programming language for syntax highlighting)
- **code**: string (the actual code content)
- **description**: string (explanation of what the code does)
- **relatedPage**: string (reference to the page containing this code)
- **tags**: array of strings (relevant topics or technologies)

### Diagram
- **id**: string (unique identifier for the diagram)
- **type**: string (mermaid, plantuml, custom-component, etc.)
- **definition**: string (the diagram definition code)
- **title**: string (title for the diagram)
- **relatedPage**: string (reference to the page containing this diagram)
- **description**: string (explanation of what the diagram shows)

## Relationships
- Course Module contains multiple Pages
- Page contains multiple Interactive Elements
- Page may contain multiple Code Examples
- Page may contain multiple Diagrams
- Interactive Elements belong to a single Page
- Code Examples belong to a single Page
- Diagrams belong to a single Page

## Validation Rules
- Module IDs must be unique across the course
- Page IDs must be unique across the course
- Module order values must be consecutive integers starting from 1
- Page order values within a module must be consecutive integers starting from 1
- All content must be in English
- All code examples must have a valid language identifier
- All pages must have a title and content