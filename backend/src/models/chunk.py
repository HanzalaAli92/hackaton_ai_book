from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ContentChunk(BaseModel):
    id: str
    content: str
    source_path: str
    source_title: str
    chunk_index: int
    embedding_vector: Optional[list] = None  # Will be set when stored in vector DB
    metadata: Optional[Dict[str, Any]] = {}
    created_at: datetime
    updated_at: datetime