from typing import List, Dict, Any
from ..services.embedding import DefaultEmbeddingService
from ..services.vector_store import VectorStoreService
from ..config import settings


class RetrievalService:
    def __init__(self):
        self.embedding_service = DefaultEmbeddingService()
        self.vector_store = VectorStoreService()
        self.top_k = 5  # Number of chunks to retrieve

    def retrieve_relevant_chunks(self,
                               query: str,
                               selected_text: str = None,
                               top_k: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant content chunks based on the query.
        """
        if top_k is None:
            top_k = self.top_k

        # Combine query and selected text if provided
        search_text = query
        if selected_text:
            search_text = f"{selected_text} {query}"

        # Generate embedding for the search text
        query_embedding = self.embedding_service.generate_embedding(search_text)

        # Search in the vector store
        results = self.vector_store.search(query_embedding, limit=top_k)

        return results

    def retrieve_with_context_augmentation(self,
                                          query: str,
                                          conversation_history: List[Dict[str, str]] = None,
                                          selected_text: str = None,
                                          top_k: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks with additional context from conversation history.
        """
        if top_k is None:
            top_k = self.top_k

        # Build enhanced query with conversation context
        enhanced_query = query
        if conversation_history:
            # Add recent conversation context to the query
            recent_context = " ".join([msg["content"] for msg in conversation_history[-2:]])
            enhanced_query = f"{recent_context} {query}"

        # Include selected text if provided
        if selected_text:
            enhanced_query = f"{selected_text} {enhanced_query}"

        # Generate embedding for the enhanced query
        query_embedding = self.embedding_service.generate_embedding(enhanced_query)

        # Search in the vector store
        results = self.vector_store.search(query_embedding, limit=top_k)

        return results

    def retrieve_with_selected_text_priority(self,
                                           query: str,
                                           selected_text: str,
                                           top_k: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve chunks with priority given to content similar to the selected text.
        This method specifically focuses on retrieving content related to the selected text.
        """
        if top_k is None:
            top_k = self.top_k

        # First, search for content similar to the selected text
        selected_text_embedding = self.embedding_service.generate_embedding(selected_text)
        selected_text_results = self.vector_store.search(selected_text_embedding, limit=top_k)

        # Then search for content similar to the query
        query_embedding = self.embedding_service.generate_embedding(query)
        query_results = self.vector_store.search(query_embedding, limit=top_k)

        # Combine results, giving priority to selected text matches
        # Create a dictionary to avoid duplicates, with relevance scores
        combined_results = {}

        # Add selected text results with potentially higher relevance
        for result in selected_text_results:
            combined_results[result["id"]] = result
            # Boost relevance score for matches with selected text
            combined_results[result["id"]]["relevance_score"] *= 1.2

        # Add query results, updating if already present
        for result in query_results:
            if result["id"] in combined_results:
                # Average the scores if it's in both result sets
                combined_results[result["id"]]["relevance_score"] = (
                    combined_results[result["id"]]["relevance_score"] + result["relevance_score"]
                ) / 2
            else:
                combined_results[result["id"]] = result

        # Sort by relevance score and return top_k
        sorted_results = sorted(
            combined_results.values(),
            key=lambda x: x["relevance_score"],
            reverse=True
        )[:top_k]

        return sorted_results

    def get_content_for_sources(self, chunk_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieve content for specific chunk IDs (useful for getting full context).
        This would require a different approach since Qdrant doesn't directly support
        fetching by ID in the same way. For now, we'll return the IDs as a reference.
        """
        # In a real implementation, you might want to store additional metadata
        # in a separate database that can be queried by chunk ID
        return [{"chunk_id": chunk_id} for chunk_id in chunk_ids]