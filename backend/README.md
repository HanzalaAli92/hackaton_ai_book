# RAG Chatbot Backend API

Backend API for the RAG (Retrieval-Augmented Generation) chatbot integrated with the Physical AI & Humanoid Robotics book.

## Overview

The backend provides APIs for the RAG chatbot functionality, including content ingestion, vector storage, and query processing for the educational content on robotics and AI.

## Features

- Content ingestion from Docusaurus docs directory
- Vector storage using Qdrant for semantic search
- Qwen embeddings for content chunks
- OpenRouter integration for LLM responses
- Text selection and context-aware querying
- Rate limiting and security controls

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Navigate to the backend directory
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the backend root with the following:

```
OPENROUTER_API_KEY=your_openrouter_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_key_here
NEON_DATABASE_URL=your_neon_connection_string_here
QDRANT_COLLECTION_NAME=book_content_chunks
```

### Running the Server

```bash
# Development mode
uvicorn src.api.main:app --reload --port 8000

# Production mode
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

The server will run on `http://localhost:8000`

## API Endpoints

- `POST /api/v1/query` - Submit a query and get a response
- `POST /api/v1/ingest` - Ingest book content into the vector store
- `POST /api/v1/ingest/refresh` - Refresh all content
- `GET /api/v1/health` - Health check endpoint

## Technologies Used

- FastAPI
- Qdrant
- HuggingFace Transformers
- OpenRouter API
- Neon Postgres