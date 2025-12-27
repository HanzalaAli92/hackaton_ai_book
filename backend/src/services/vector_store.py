from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from ..config import settings


class VectorStoreService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = settings.qdrant_collection_name
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection if it doesn't exist."""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,  # Size for sentence-transformers/all-MiniLM-L6-v2
                    distance=models.Distance.COSINE
                )
            )

    def upsert_chunk(self, chunk_id: str, content: str, embedding: List[float], metadata: Dict[str, Any]):
        """Upsert a content chunk with its embedding to the vector store."""
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "source_path": metadata.get("source_path", ""),
                        "source_title": metadata.get("source_title", ""),
                        "chunk_index": metadata.get("chunk_index", 0),
                        "created_at": metadata.get("created_at", datetime.now().isoformat()),
                        "updated_at": metadata.get("updated_at", datetime.now().isoformat()),
                        "word_count": metadata.get("word_count", 0),
                        "section_type": metadata.get("section_type", "content"),
                        **metadata.get("additional_metadata", {})
                    }
                )
            ]
        )

    def upsert_chunks(self, chunks_data: List[Dict[str, Any]]):
        """Upsert multiple content chunks with their embeddings to the vector store."""
        points = []
        for chunk_data in chunks_data:
            points.append(models.PointStruct(
                id=chunk_data["chunk_id"],
                vector=chunk_data["embedding"],
                payload={
                    "content": chunk_data["content"],
                    "source_path": chunk_data["metadata"].get("source_path", ""),
                    "source_title": chunk_data["metadata"].get("source_title", ""),
                    "chunk_index": chunk_data["metadata"].get("chunk_index", 0),
                    "created_at": chunk_data["metadata"].get("created_at", datetime.now().isoformat()),
                    "updated_at": chunk_data["metadata"].get("updated_at", datetime.now().isoformat()),
                    "word_count": chunk_data["metadata"].get("word_count", 0),
                    "section_type": chunk_data["metadata"].get("section_type", "content"),
                    **chunk_data["metadata"].get("additional_metadata", {})
                }
            ))

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar content chunks based on the query embedding."""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True
        )

        return [
            {
                "id": result.id,
                "content": result.payload["content"],
                "source_path": result.payload["source_path"],
                "source_title": result.payload["source_title"],
                "chunk_index": result.payload["chunk_index"],
                "relevance_score": result.score,
                "metadata": {k: v for k, v in result.payload.items()
                           if k not in ["content", "source_path", "source_title", "chunk_index"]}
            }
            for result in results
        ]

    def delete_collection(self):
        """Delete the entire collection (useful for refresh operations)."""
        try:
            self.client.delete_collection(self.collection_name)
            self._initialize_collection()  # Recreate empty collection
            return True
        except Exception:
            return False

    def get_chunk_count(self) -> int:
        """Get the total number of chunks in the collection."""
        collection_info = self.client.get_collection(self.collection_name)
        return collection_info.points_count

    def delete_chunks_by_source(self, source_path: str):
        """Delete all chunks from a specific source path."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="source_path",
                            match=models.MatchValue(value=source_path)
                        )
                    ]
                )
            )
        )