from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class QuerySession(BaseModel):
    id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    expires_at: datetime


class QueryMessage(BaseModel):
    id: str
    session_id: str
    role: str  # "user" or "assistant"
    content: str
    retrieved_chunks: Optional[List[str]] = []
    timestamp: datetime


class QueryRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None
    context_window: Optional[int] = 3


class QueryResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    session_id: str
    followup_questions: List[str]