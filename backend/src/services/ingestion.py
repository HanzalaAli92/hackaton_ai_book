from typing import List, Dict, Any
from ..utils.markdown_parser import parse_markdown_with_sections, get_all_markdown_files
from ..utils.text_splitter import split_markdown_content
from ..services.embedding import DefaultEmbeddingService
from ..services.vector_store import VectorStoreService
from ..models.chunk import ContentChunk
from datetime import datetime
import hashlib
import uuid
import logging
from ..config import settings


class IngestionService:
    def __init__(self):
        self.embedding_service = DefaultEmbeddingService()
        self.vector_store = VectorStoreService()
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap

    def ingest_documents(self, docs_path: str) -> Dict[str, Any]:
        """
        Ingest all markdown documents from the specified path.
        """
        # Get all markdown files
        markdown_files = get_all_markdown_files(docs_path)
        total_files = len(markdown_files)

        logging.info(f"Found {total_files} markdown files to process")

        total_chunks = 0
        processed_files = 0

        for file_path in markdown_files:
            try:
                # Parse the markdown file into sections
                sections = parse_markdown_with_sections(file_path)

                for section in sections:
                    # Split the content into chunks
                    content_chunks = split_markdown_content(
                        section['content'],
                        chunk_size=self.chunk_size,
                        chunk_overlap=self.chunk_overlap
                    )

                    # Process each chunk
                    for i, chunk_content in enumerate(content_chunks):
                        chunk_id = str(uuid.uuid4())

                        # Generate embedding for the chunk
                        embedding = self.embedding_service.generate_embedding(chunk_content)

                        # Create metadata for the chunk
                        content_hash = hashlib.md5(chunk_content.encode()).hexdigest()
                        metadata = {
                            "source_path": file_path,
                            "source_title": section['title'],
                            "chunk_index": i,
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat(),
                            "word_count": len(chunk_content.split()),
                            "section_type": section['type'],
                            "content_hash": content_hash,
                            "additional_metadata": section.get('frontmatter', {})
                        }

                        # Upsert the chunk to vector store
                        self.vector_store.upsert_chunk(
                            chunk_id=chunk_id,
                            content=chunk_content,
                            embedding=embedding,
                            metadata=metadata
                        )

                        total_chunks += 1

                processed_files += 1
                logging.info(f"Processed file {processed_files}/{total_files}: {file_path}")

            except Exception as e:
                logging.error(f"Error processing file {file_path}: {str(e)}")
                continue

        return {
            "status": "success",
            "chunks_processed": total_chunks,
            "documents_processed": processed_files,
            "message": f"Content ingestion completed successfully. Processed {processed_files} documents and {total_chunks} chunks."
        }

    def refresh_documents(self, docs_path: str) -> Dict[str, Any]:
        """
        Refresh all content by deleting existing and re-ingesting.
        """
        # Get the count before deletion
        chunks_before = self.vector_store.get_chunk_count()

        # Delete the existing collection
        success = self.vector_store.delete_collection()
        if not success:
            return {
                "status": "error",
                "message": "Failed to delete existing collection"
            }

        # Ingest the documents again
        result = self.ingest_documents(docs_path)
        result["chunks_deleted"] = chunks_before

        return result

    def update_document(self, file_path: str) -> Dict[str, Any]:
        """
        Update a single document by deleting its chunks and re-ingesting.
        """
        # Delete existing chunks for this source
        self.vector_store.delete_chunks_by_source(file_path)

        # Parse and re-ingest the document
        sections = parse_markdown_with_sections(file_path)
        total_chunks = 0

        for section in sections:
            # Split the content into chunks
            content_chunks = split_markdown_content(
                section['content'],
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

            # Process each chunk
            for i, chunk_content in enumerate(content_chunks):
                chunk_id = str(uuid.uuid4())

                # Generate embedding for the chunk
                embedding = self.embedding_service.generate_embedding(chunk_content)

                # Create metadata for the chunk
                content_hash = hashlib.md5(chunk_content.encode()).hexdigest()
                metadata = {
                    "source_path": file_path,
                    "source_title": section['title'],
                    "chunk_index": i,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "word_count": len(chunk_content.split()),
                    "section_type": section['type'],
                    "content_hash": content_hash,
                    "additional_metadata": section.get('frontmatter', {})
                }

                # Upsert the chunk to vector store
                self.vector_store.upsert_chunk(
                    chunk_id=chunk_id,
                    content=chunk_content,
                    embedding=embedding,
                    metadata=metadata
                )

                total_chunks += 1

        return {
            "status": "success",
            "chunks_processed": total_chunks,
            "document_path": file_path,
            "message": f"Document updated successfully. Processed {total_chunks} chunks."
        }

    def validate_ingestion(self) -> Dict[str, Any]:
        """
        Validate the ingestion by checking the vector store.
        """
        chunk_count = self.vector_store.get_chunk_count()
        return {
            "status": "success",
            "total_chunks": chunk_count,
            "message": f"Validation successful. Vector store contains {chunk_count} chunks."
        }