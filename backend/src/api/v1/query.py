from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import logging
from ...services.retrieval import RetrievalService
from ...services.llm import LLMService
from ...models.query import QueryRequest, QueryResponse


router = APIRouter(prefix="/query", tags=["query"])


@router.post("/", response_model=QueryResponse)
async def query_content(request: QueryRequest):
    """
    Submit a query and receive an AI-generated response based on book content.
    """
    try:
        # Validate input
        if not request.query or len(request.query.strip()) < 5:
            raise HTTPException(status_code=400, detail="Query must be at least 5 characters long")

        if request.selected_text and len(request.selected_text) > 1000:
            raise HTTPException(status_code=400, detail="Selected text must be less than 1000 characters")

        # Initialize services
        retrieval_service = RetrievalService()
        llm_service = LLMService()

        # Retrieve relevant chunks
        if request.selected_text:
            # If selected text is provided, use the priority method
            relevant_chunks = retrieval_service.retrieve_with_selected_text_priority(
                query=request.query,
                selected_text=request.selected_text
            )
        else:
            # Otherwise, use the standard method
            relevant_chunks = retrieval_service.retrieve_relevant_chunks(
                query=request.query,
                selected_text=request.selected_text
            )

        if not relevant_chunks:
            # If no relevant chunks found, return a message indicating this
            return QueryResponse(
                response="I couldn't find relevant information in the book content to answer your question.",
                sources=[],
                session_id=request.session_id or str(uuid.uuid4()),
                followup_questions=[]
            )

        # Generate response using LLM
        response_text = llm_service.generate_response(
            query=request.query,
            context_chunks=relevant_chunks,
            selected_text=request.selected_text
        )

        # Generate follow-up questions
        followup_questions = llm_service.generate_followup_questions(
            query=request.query,
            response=response_text,
            context_chunks=relevant_chunks
        )

        # Prepare sources for response
        sources = [
            {
                "source_path": chunk["source_path"],
                "source_title": chunk["source_title"],
                "relevance_score": chunk["relevance_score"]
            }
            for chunk in relevant_chunks
        ]

        # Generate or use session ID
        session_id = request.session_id or str(uuid.uuid4())

        return QueryResponse(
            response=response_text,
            sources=sources,
            session_id=session_id,
            followup_questions=followup_questions
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your query")


@router.post("/with-context")
async def query_with_context(request: QueryRequest):
    """
    Submit a query with conversation context and receive a response.
    """
    try:
        # This endpoint would handle queries with full conversation context
        # For now, it works similarly to the basic query but could be enhanced
        # to better handle context window and conversation history
        return await query_content(request)
    except Exception as e:
        logging.error(f"Error processing query with context: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your query")