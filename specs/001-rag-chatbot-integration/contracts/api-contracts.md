# API Contracts: RAG Chatbot Integration

## Base URL
`http://localhost:8000/api/v1` (development)
`https://your-backend-url/api/v1` (production)

## Authentication
All endpoints require API key in header: `Authorization: Bearer {api_key}`

## Endpoints

### Ingestion

#### POST /ingest
**Description**: Ingest content from Docusaurus docs directory into vector store

**Request**:
```json
{
  "docs_path": "/path/to/docs/directory",
  "chunk_size": 500,
  "chunk_overlap": 50
}
```

**Response**:
```json
{
  "status": "success",
  "chunks_processed": 150,
  "documents_processed": 12,
  "message": "Content ingestion completed successfully"
}
```

**Error Responses**:
- `400`: Invalid request parameters
- `500`: Ingestion failed

#### POST /ingest/refresh
**Description**: Refresh all content by deleting existing and re-ingesting

**Request**:
```json
{
  "docs_path": "/path/to/docs/directory",
  "chunk_size": 500,
  "chunk_overlap": 50
}
```

**Response**:
```json
{
  "status": "success",
  "chunks_deleted": 120,
  "chunks_processed": 150,
  "documents_processed": 12,
  "message": "Content refresh completed successfully"
}
```

### Query

#### POST /query
**Description**: Submit a query and receive an AI-generated response based on book content

**Request**:
```json
{
  "query": "What is ROS 2?",
  "selected_text": "Optional text selected by user",
  "session_id": "optional-session-id",
  "context_window": 3
}
```

**Response**:
```json
{
  "response": "ROS 2 is a set of software libraries and tools that help you build robot applications...",
  "sources": [
    {
      "source_path": "/module-1-robotic-nervous-system/ros2-nodes-topics.md",
      "source_title": "ROS 2 Nodes, Topics, and Services",
      "relevance_score": 0.92
    }
  ],
  "session_id": "new-or-existing-session-id",
  "followup_questions": [
    "What are the main components of ROS 2?",
    "How does ROS 2 differ from ROS 1?"
  ]
}
```

**Error Responses**:
- `400`: Invalid query parameters
- `429`: Rate limit exceeded
- `500`: Query processing failed

### Health

#### GET /health
**Description**: Check the health status of the service

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-26T10:30:00Z",
  "version": "1.0.0",
  "dependencies": {
    "qdrant": "connected",
    "neon": "connected",
    "openrouter": "available"
  }
}
```

## Data Models

### QueryRequest
```json
{
  "query": {
    "type": "string",
    "minLength": 5,
    "maxLength": 500,
    "required": true
  },
  "selected_text": {
    "type": "string",
    "maxLength": 1000,
    "required": false
  },
  "session_id": {
    "type": "string",
    "format": "uuid",
    "required": false
  },
  "context_window": {
    "type": "integer",
    "minimum": 1,
    "maximum": 10,
    "default": 3,
    "required": false
  }
}
```

### QueryResponse
```json
{
  "response": {
    "type": "string",
    "required": true
  },
  "sources": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "source_path": {
          "type": "string",
          "required": true
        },
        "source_title": {
          "type": "string",
          "required": true
        },
        "relevance_score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "required": true
        }
      }
    },
    "required": true
  },
  "session_id": {
    "type": "string",
    "format": "uuid",
    "required": true
  },
  "followup_questions": {
    "type": "array",
    "items": {
      "type": "string"
    },
    "required": true
  }
}
```

## Rate Limiting
- Per-user rate limits: 100 requests per minute
- Burst allowance: 10 requests
- Headers returned: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset

## Error Format
All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Optional detailed error information"
  }
}
```

Common error codes:
- `INVALID_INPUT`: Request parameters are invalid
- `RATE_LIMIT_EXCEEDED`: Request rate limit exceeded
- `VECTOR_STORE_ERROR`: Issue with vector store operations
- `LLM_ERROR`: Issue with LLM service
- `INTERNAL_ERROR`: Unexpected internal error