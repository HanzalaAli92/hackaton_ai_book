# Data Model: RAG Chatbot Integration

## Entities

### ContentChunk
- **id**: string (UUID) - Unique identifier for the content chunk
- **content**: string - The actual text content of the chunk
- **source_path**: string - File path in the docs directory where the content originates
- **source_title**: string - Title of the source document
- **chunk_index**: integer - Position of this chunk within the source document
- **embedding_vector**: array<float> - Vector representation of the content (for Qdrant)
- **metadata**: object - Additional metadata (word_count, section_type, etc.)
- **created_at**: datetime - Timestamp of when the chunk was created
- **updated_at**: datetime - Timestamp of last update

### QuerySession
- **id**: string (UUID) - Unique identifier for the conversation session
- **user_id**: string (optional) - Identifier for the user (for rate limiting)
- **created_at**: datetime - When the session was started
- **updated_at**: datetime - When the session was last updated
- **expires_at**: datetime - When the session expires

### QueryMessage
- **id**: string (UUID) - Unique identifier for the message
- **session_id**: string - Reference to the parent QuerySession
- **role**: string (enum: "user", "assistant") - Who sent the message
- **content**: string - The message content
- **retrieved_chunks**: array<string> - IDs of chunks used to generate the response
- **timestamp**: datetime - When the message was created

### QueryRequest
- **query**: string - The user's question
- **selected_text**: string (optional) - Text the user selected on the page
- **session_id**: string (optional) - ID of the conversation session
- **context_window**: integer (default: 3) - Number of previous messages to include in context

### QueryResponse
- **response**: string - The AI-generated answer
- **sources**: array<object> - List of sources used in the response
  - **source_path**: string - Path to the source document
  - **source_title**: string - Title of the source
  - **relevance_score**: float - How relevant this source was to the response
- **session_id**: string - ID of the conversation session
- **followup_questions**: array<string> - Suggested follow-up questions

## Relationships

- QuerySession (1) → (Many) QueryMessage
- QueryMessage (Many) → (Many) ContentChunk (via retrieved_chunks)

## Validation Rules

### ContentChunk
- content must be between 50 and 2000 tokens
- source_path must exist in the docs directory
- embedding_vector must have the correct dimensions for the chosen model

### QueryRequest
- query must be between 5 and 500 characters
- selected_text (if provided) must be between 10 and 1000 characters
- session_id (if provided) must reference an existing active session

### QueryMessage
- content must be between 1 and 5000 characters
- role must be either "user" or "assistant"
- session_id must reference an existing active session