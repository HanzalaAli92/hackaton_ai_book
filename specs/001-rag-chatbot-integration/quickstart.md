# Quickstart Guide: RAG Chatbot Integration

## Prerequisites

- Python 3.11+
- Node.js 18+
- Access to Open Router API key
- Access to Qdrant Cloud account
- Access to Neon Postgres account

## Backend Setup

### 1. Environment Configuration
```bash
cd backend
cp .env.example .env
# Edit .env with your API keys and connection strings:
# OPENROUTER_API_KEY=your_openrouter_key
# QDRANT_URL=your_qdrant_url
# QDRANT_API_KEY=your_qdrant_key
# NEON_DATABASE_URL=your_neon_connection_string
```

### 2. Installation
```bash
pip install fastapi uvicorn python-dotenv transformers torch psycopg2-binary qdrant-client openai
```

### 3. Run Backend Server
```bash
uvicorn src.api.main:app --reload --port 8000
```

## Frontend Integration

### 1. Install Chat Widget
```bash
cd frontend/website
npm install # if dependencies haven't been installed
```

### 2. Add to Docusaurus Configuration
Update `docusaurus.config.ts` to include the chat widget:

```typescript
// In the plugins section
plugins: [
  // ... existing plugins
  [
    '@docusaurus/plugin-content-pages',
    {
      // ... existing config
    },
  ],
],

// Add the chat widget to the theme config
themeConfig: {
  // ... existing theme config
  chatWidget: {
    enabled: true,
    backendUrl: 'http://localhost:8000', // Update for production
  },
},
```

### 3. Add Component Import
In your layout or main page component:

```tsx
import ChatWidget from './src/components/ChatWidget/ChatWidget';

// Use in your JSX
<ChatWidget />
```

## Content Ingestion

### 1. Prepare Content
Ensure your book content is in the `docs/` directory in Markdown format.

### 2. Run Ingestion Script
```bash
cd backend
python -m src.services.ingestion --docs-path ../frontend/website/docs
```

This will:
- Parse all Markdown files in the docs directory
- Split content into 500-token chunks
- Generate embeddings using Qwen model
- Store chunks in Qdrant vector database
- Store metadata in Neon Postgres

## API Endpoints

### Ingestion
- `POST /api/v1/ingest` - Ingest content from docs directory
- `POST /api/v1/ingest/refresh` - Refresh all content (deletes existing)

### Query
- `POST /api/v1/query` - Submit a query and get response
- `GET /api/v1/health` - Check service health

Example query:
```json
{
  "query": "What is ROS 2?",
  "selected_text": "ROS 2 is a set of software libraries and tools",
  "session_id": "optional-session-id"
}
```

## Frontend Integration

The chat widget can be embedded in any page and provides:
- Text selection capture
- Conversation history
- Source citations
- Follow-up suggestions

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend/website
npm test
```

## Deployment

### Backend
Deploy to Vercel or Heroku with environment variables set:
- OPENROUTER_API_KEY
- QDRANT_URL
- QDRANT_API_KEY
- NEON_DATABASE_URL

### Frontend
The chat widget will work with the existing GitHub Pages deployment, just ensure CORS is configured for the backend URL.