# Research: RAG Chatbot Integration

## Decision: Technology Stack Selection

**Rationale**: Selected FastAPI for backend due to its async support, excellent documentation, and Pydantic integration. Qdrant for vector storage due to its performance and cloud offering. Qwen embeddings via HuggingFace for cost-effective and accurate embeddings. Open Router for LLM access to multiple models with unified API.

**Alternatives considered**:
- Backend: Flask vs FastAPI - FastAPI chosen for better async performance and built-in OpenAPI docs
- Vector DB: Pinecone vs Qdrant vs Weaviate - Qdrant chosen for free tier and good performance
- Embeddings: OpenAI vs HuggingFace transformers - Qwen via HF chosen for cost and performance
- Frontend: Vanilla JS vs React components - React chosen for better maintainability

## Decision: Content Chunking Strategy

**Rationale**: Using 500-token chunks with 50-token overlap to balance context retention with retrieval precision. This size allows for coherent semantic units while maintaining efficient vector search.

**Alternatives considered**:
- Chunk sizes: 200, 500, 1000 tokens - 500 chosen as sweet spot for technical content
- Overlap: 0, 25, 50 tokens - 50 chosen to maintain context across chunks

## Decision: Text Selection Integration

**Rationale**: Implementing via JavaScript event listeners that capture text selection and pass context to the query endpoint. This provides contextual Q&A capability without disrupting the reading experience.

**Alternatives considered**:
- Browser extension vs in-page integration - chose in-page for simplicity
- Click vs selection-based queries - chose selection for natural UX

## Decision: Deployment Architecture

**Rationale**: Separate backend deployment (Vercel/Heroku) with CORS configuration for GitHub Pages frontend. This ensures security (API keys not exposed client-side) while maintaining frontend accessibility.

**Alternatives considered**:
- Monolithic vs microservice - chose separate services for security
- Different hosting options - GitHub Pages for frontend is free and reliable