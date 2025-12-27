# Implementation Plan: RAG Chatbot Integration

**Branch**: `001-rag-chatbot-integration` | **Date**: 2025-12-26 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Retrieval-Augmented Generation (RAG) chatbot for the Physical AI & Humanoid Robotics educational book. The system will allow students to ask questions about book content and receive accurate answers based on the course material. The architecture includes a FastAPI backend with Neon Postgres for metadata, Qdrant for vector storage, Qwen embeddings, and Open Router for LLM responses. The frontend will feature a React-based chat widget integrated into the Docusaurus site with text selection capabilities.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript 5.0+ (Frontend)
**Primary Dependencies**: FastAPI, Neon Postgres, Qdrant, Transformers (HuggingFace), Open Router API, React, Docusaurus
**Storage**: Neon Serverless Postgres (metadata), Qdrant Cloud (vector embeddings), Docusaurus docs directory (source content)
**Testing**: pytest (Backend), Jest/React Testing Library (Frontend)
**Target Platform**: Linux server (Backend), Web browser (Frontend)
**Project Type**: Web application (separate backend + frontend)
**Performance Goals**: <5 second response time for 95% of queries, support 100 concurrent users
**Constraints**: <200ms p95 for vector search, API rate limiting to control costs, GitHub Pages integration for frontend
**Scale/Scope**: 1000+ book content chunks, 100 concurrent users, 90% accuracy in content retrieval

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Educational Content Quality**: The RAG system will enhance educational content by providing interactive Q&A capabilities while maintaining technical accuracy of the Physical AI & Humanoid Robotics course.
- **Docusaurus-Based Structure**: The chatbot will integrate seamlessly with the existing Docusaurus v3+ structure using React components and MDX integration.
- **Technical Accuracy and Non-Hallucination**: The RAG system will only provide answers based on retrieved content from the book, preventing hallucinations and ensuring technical accuracy.
- **Modularity and Version Control**: The chatbot will be implemented as a modular component that can be versioned independently while maintaining Git-based version control.
- **Professional Tone and Accessibility**: The chat interface will maintain professional educational tone and be accessible to students.
- **Deployment and Distribution**: The backend will be deployed separately (Vercel/Heroku) with CORS configuration for GitHub Pages frontend integration.

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── chunk.py          # Content chunk data model
│   │   ├── query.py          # Query request/response models
│   │   └── metadata.py       # Metadata for content chunks
│   ├── services/
│   │   ├── ingestion.py      # Content ingestion and processing service
│   │   ├── embedding.py      # Qwen embedding service
│   │   ├── vector_store.py   # Qdrant vector store operations
│   │   ├── retrieval.py      # Content retrieval service
│   │   └── llm.py            # Open Router LLM service
│   ├── api/
│   │   ├── v1/
│   │   │   ├── router.py
│   │   │   ├── ingest.py     # Ingestion endpoints
│   │   │   ├── query.py      # Query endpoints
│   │   │   └── health.py     # Health check endpoints
│   │   └── main.py           # FastAPI app entry point
│   └── utils/
│       ├── text_splitter.py  # Text chunking utilities
│       └── markdown_parser.py # Markdown parsing utilities
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── website/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWidget/
│   │   │   │   ├── ChatWidget.tsx
│   │   │   │   ├── ChatWidget.module.css
│   │   │   │   ├── Message.tsx
│   │   │   │   └── InputArea.tsx
│   │   │   └── TextSelectionHandler/
│   │   │       └── TextSelectionHandler.tsx
│   │   ├── pages/
│   │   └── services/
│   │       └── api-client.ts  # API client for backend communication
│   ├── docs/                  # Existing book content
│   ├── docusaurus.config.ts
│   ├── sidebars.ts
│   └── package.json
└── README.md
```

**Structure Decision**: Selected web application structure with separate backend (FastAPI) and frontend (Docusaurus React components) to maintain clear separation of concerns. The backend handles RAG processing while the frontend provides the user interface integrated into the existing Docusaurus book.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Separate backend service | Security and performance requirements | Embedding all logic in frontend would expose API keys and be too slow |
| Multiple data stores (Neon + Qdrant) | Specialized storage needs for metadata vs vectors | Single store would compromise performance for either metadata queries or vector search |
