---
id: 1
title: rag-chatbot-integration-plan
stage: plan
date: '2025-12-26'
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot-integration
branch: 001-rag-chatbot-integration
user: Claude Sonnet 4.5
command: /sp.plan
labels:
  - planning
  - rag
  - chatbot
  - architecture
  - api
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot-integration/plan.md
  - specs/001-rag-chatbot-integration/research.md
  - specs/001-rag-chatbot-integration/data-model.md
  - specs/001-rag-chatbot-integration/quickstart.md
  - specs/001-rag-chatbot-integration/contracts/api-contracts.md
tests: []
---

# RAG Chatbot Integration Planning

## Prompt

```
Create a detailed technical implementation plan for integrating the RAG Chatbot into the Docusaurus book "Physical AI & Humanoid Robotics".

Align with spec: Use FastAPI backend, Neon Postgres for metadata, Qdrant for vectors, Qwen for embeddings (HuggingFace integration), Open Router API for LLM calls.

Architecture:
- Ingestion: Script to parse Docusaurus docs/ Markdown, chunk text, embed with Qwen, upsert to Qdrant, metadata to Neon.
- Backend: FastAPI endpoints for /ingest, /query (retrieve from Qdrant, augment, call Open Router).
- Frontend: React-based chat widget using ChatKit SDK adapted for Open Router, embed in Docusaurus via custom component or plugin.
- Handle selected text: JS event listener to capture selection, pass as context to query.
- Decisions: Chunk size ~500 tokens, hybrid search if needed, error handling for free tiers.
- Deployment: Backend separate repo, CORS for GitHub Pages integration.

Break down: Data flow, APIs, components, and alignment with constitution.
```

## Response

Completed comprehensive technical implementation plan for RAG Chatbot integration including:

- Detailed architecture with FastAPI backend, Neon Postgres, Qdrant vector store
- Complete project structure with separate backend/frontend
- Research document with technology decisions and alternatives
- Data models for content chunks, query sessions, and messages
- API contracts with full endpoint specifications
- Quickstart guide for setup and deployment
- Constitution alignment ensuring educational quality and technical accuracy

The plan is ready for task breakdown and implementation.