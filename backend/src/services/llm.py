import openrouter
from typing import List, Dict, Any
import logging
from ..config import settings


class LLMService:
    def __init__(self):
        self.client = openrouter.OpenRouter(api_key=settings.openrouter_api_key)

    def generate_response(self,
                         query: str,
                         context_chunks: List[Dict[str, Any]],
                         selected_text: str = None,
                         conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response based on the query and context chunks.
        """
        # Build the context from retrieved chunks
        context_text = "\n\n".join([chunk["content"] for chunk in context_chunks])

        # Build the prompt
        prompt = self._build_prompt(query, context_text, selected_text, conversation_history)

        try:
            # Call the OpenRouter API
            response = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo",  # You can change this to any supported model
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant for the Physical AI & Humanoid Robotics educational book. "
                            "Your purpose is to answer student questions about the book content based on the provided context. "
                            "Always be helpful, accurate, and cite sources when possible. "
                            "If the answer is not in the provided context, say so clearly."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"Error calling LLM API: {str(e)}")
            raise

    def _build_prompt(self,
                     query: str,
                     context: str,
                     selected_text: str = None,
                     conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Build the prompt for the LLM based on query, context, and other factors.
        """
        prompt_parts = []

        # Add conversation history if available
        if conversation_history:
            prompt_parts.append("Previous conversation:")
            for msg in conversation_history[-3:]:  # Use last 3 exchanges
                role = "Student" if msg["role"] == "user" else "Assistant"
                prompt_parts.append(f"{role}: {msg['content']}")
            prompt_parts.append("\n")

        # Add selected text context if provided
        if selected_text:
            prompt_parts.append(f"Selected text for context: {selected_text}\n\n")

        # Add the main query
        prompt_parts.append(f"Question: {query}\n\n")

        # Add the retrieved context
        prompt_parts.append("Relevant context from the book:")
        prompt_parts.append(context)

        # Add instruction for the response
        prompt_parts.append(
            "\nPlease answer the question based on the provided context. "
            "If the answer is not in the context, say so clearly. "
            "Cite the relevant sections when possible."
        )

        return "\n".join(prompt_parts)

    def generate_followup_questions(self,
                                  query: str,
                                  response: str,
                                  context_chunks: List[Dict[str, Any]]) -> List[str]:
        """
        Generate follow-up questions based on the query, response, and context.
        """
        prompt = (
            f"Based on this query: '{query}'\n"
            f"And this response: '{response}'\n"
            f"About this topic: {'; '.join([chunk['source_title'] for chunk in context_chunks[:2]])}\n"
            "Generate 3 follow-up questions that a student might ask. "
            "Provide only the questions, one per line, without any additional text."
        )

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant for the Physical AI & Humanoid Robotics educational book. "
                            "Your task is to generate follow-up questions that help students explore the topic further."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=200
            )

            # Parse the response into individual questions
            questions_text = response.choices[0].message.content
            questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
            return questions[:3]  # Return maximum 3 questions

        except Exception as e:
            logging.error(f"Error generating follow-up questions: {str(e)}")
            return []  # Return empty list if generation fails