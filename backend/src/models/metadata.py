from pydantic import BaseModel
from typing import Optional, Dict, Any


class ContentMetadata(BaseModel):
    source_path: str
    source_title: str
    word_count: int
    section_type: str
    content_hash: str
    created_at: str
    updated_at: str
    additional_metadata: Optional[Dict[str, Any]] = {}