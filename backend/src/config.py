from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Configuration
    openrouter_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    neon_database_url: str
    qdrant_collection_name: str = "book_content_chunks"

    # Application Configuration
    app_name: str = "RAG Chatbot API"
    debug: bool = False
    version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    # Processing Configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    max_query_length: int = 500
    max_selected_text_length: int = 1000

    class Config:
        env_file = ".env"


settings = Settings()