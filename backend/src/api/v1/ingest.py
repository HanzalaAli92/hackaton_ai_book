from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ...services.ingestion import IngestionService
from ...config import settings


router = APIRouter(prefix="/ingest", tags=["ingestion"])


class IngestRequest(BaseModel):
    docs_path: str
    chunk_size: Optional[int] = settings.chunk_size
    chunk_overlap: Optional[int] = settings.chunk_overlap


class RefreshRequest(BaseModel):
    docs_path: str
    chunk_size: Optional[int] = settings.chunk_size
    chunk_overlap: Optional[int] = settings.chunk_overlap


@router.post("/")
async def ingest_content(request: IngestRequest):
    """
    Ingest content from Docusaurus docs directory into vector store.
    """
    try:
        ingestion_service = IngestionService()
        result = ingestion_service.ingest_documents(request.docs_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh")
async def refresh_content(request: RefreshRequest):
    """
    Refresh all content by deleting existing and re-ingesting.
    """
    try:
        ingestion_service = IngestionService()
        result = ingestion_service.refresh_documents(request.docs_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/validate")
async def validate_ingestion():
    """
    Validate the ingestion by checking the vector store.
    """
    try:
        ingestion_service = IngestionService()
        result = ingestion_service.validate_ingestion()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))