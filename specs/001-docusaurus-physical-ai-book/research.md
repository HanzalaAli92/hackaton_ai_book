# Research: Physical AI & Humanoid Robotics Book Implementation

## Decision: Docusaurus v3 with Classic Theme
**Rationale**: Docusaurus v3 provides the latest features, TypeScript support, and strong Markdown/MDX capabilities. The classic theme offers good default styling with customization options for educational content.

**Alternatives considered**:
- Docusaurus v2: Would work but lacks newer features and TypeScript-first approach
- Custom React site: More complex to maintain and deploy
- GitBook: Less flexible for custom components and interactive elements

## Decision: MDX for Content Integration
**Rationale**: MDX allows embedding React components directly in Markdown, perfect for interactive diagrams, code examples, and simulations. Essential for meeting the requirement for interactive learning elements.

**Alternatives considered**:
- Pure Markdown: Would limit interactivity needed for educational content
- Static HTML: Less maintainable and harder to version control
- VuePress: Less ecosystem support for React components

## Decision: Mermaid for Diagrams
**Rationale**: Mermaid is natively supported in Docusaurus and perfect for creating flowcharts, sequence diagrams, and other visual representations of ROS flows, URDF structures, and system architectures.

**Alternatives considered**:
- Static images: Less maintainable and not responsive to content changes
- Draw.io: Requires external tool and static exports
- Custom SVG components: More complex to maintain

## Decision: GitHub Pages Deployment
**Rationale**: GitHub Pages provides free hosting, integrates well with Git workflow, and offers custom domain support. Aligns with the constitution requirement for deployment via gh-pages branch.

**Alternatives considered**:
- Netlify: Would require additional setup and configuration
- Vercel: Good alternative but GitHub Pages is sufficient for static content
- Self-hosted: Unnecessary complexity for educational content

## Decision: Folder Structure by Modules
**Rationale**: Organizing content by the four main course modules (plus overview and capstone) follows the natural curriculum structure and supports the modularity requirement from the constitution.

**Alternatives considered**:
- Chronological order: Less intuitive for navigation
- Topic-based: Would not align with course structure
- Flat structure: Would be harder to maintain and navigate

## Decision: Custom React Components for Interactivity
**Rationale**: Custom components allow for interactive code blocks, simulation viewers, and other educational tools that enhance the learning experience as required by the specification.

**Alternatives considered**:
- Third-party embeds: Less control and potential reliability issues
- Static content only: Would not meet the interactive learning requirements
- External tools: Would create dependency and maintenance overhead