import re
from typing import List, Tuple
from typing import Optional


class TextSplitter:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Split text into chunks with overlap.

        Returns:
            List of tuples containing (chunk_text, start_index, end_index)
        """
        if not text:
            return []

        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        current_start = 0
        current_position = 0

        for para in paragraphs:
            # Add the paragraph to current chunk if it doesn't exceed chunk_size
            if len(current_chunk + para) <= self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                # If adding the paragraph exceeds chunk_size, start a new chunk
                if current_chunk:
                    chunks.append((current_chunk.strip(), current_start, current_position))

                # Start new chunk with overlap from previous chunk
                overlap_start = max(0, len(current_chunk) - self.chunk_overlap)
                overlap_text = current_chunk[overlap_start:] if len(current_chunk) > self.chunk_overlap else current_chunk
                current_chunk = overlap_text + para + "\n\n"
                current_start = current_position - len(overlap_text)

            current_position += len(para) + 2  # +2 for the \n\n

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append((current_chunk.strip(), current_start, current_position))

        # If we still have large chunks that exceed the limit, split them by sentences
        final_chunks = []
        for chunk_text, start, end in chunks:
            if len(chunk_text) > self.chunk_size:
                sentence_chunks = self._split_by_sentences(chunk_text)
                for sent_chunk in sentence_chunks:
                    if len(sent_chunk) <= self.chunk_size:
                        final_chunks.append(sent_chunk)
                    else:
                        # If sentence is still too long, split by words
                        word_chunks = self._split_by_words(sent_chunk)
                        final_chunks.extend(word_chunks)
            else:
                final_chunks.append((chunk_text, start, end))

        return final_chunks

    def _split_by_sentences(self, text: str) -> List[Tuple[str, int, int]]:
        """Split text by sentences."""
        sentences = re.split(r'[.!?]+\s+', text)
        chunks = []
        current_pos = 0

        for sentence in sentences:
            sentence_with_punct = sentence
            # Add back the punctuation that was removed by split
            if sentence and current_pos + len(sentence) < len(text):
                next_char = text[current_pos + len(sentence)]
                if next_char in '.!?':
                    sentence_with_punct += next_char
                    if current_pos + len(sentence) + 1 < len(text) and text[current_pos + len(sentence) + 1] == ' ':
                        sentence_with_punct += ' '

            if len(sentence_with_punct) > self.chunk_size:
                # If sentence is too long, split by words
                word_chunks = self._split_by_words(sentence_with_punct)
                chunks.extend(word_chunks)
            else:
                chunks.append((sentence_with_punct, current_pos, current_pos + len(sentence_with_punct)))

            current_pos += len(sentence_with_punct)

        return chunks

    def _split_by_words(self, text: str) -> List[Tuple[str, int, int]]:
        """Split text by words when sentence splitting is not enough."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_chunk_len = 0
        current_pos = 0

        for word in words:
            if current_chunk_len + len(word) <= self.chunk_size or not current_chunk:
                current_chunk.append(word)
                current_chunk_len += len(word) + 1  # +1 for space
            else:
                chunk_text = ' '.join(current_chunk)
                chunks.append((chunk_text, current_pos, current_pos + len(chunk_text)))

                # Start new chunk with overlap
                overlap_size = max(0, min(self.chunk_overlap, len(current_chunk)))
                current_chunk = current_chunk[-overlap_size:] if overlap_size > 0 else []
                current_chunk.append(word)
                current_chunk_len = sum(len(w) + 1 for w in current_chunk) - 1  # Remove extra space

                current_pos += len(chunk_text) + 1  # +1 for the separating space

        # Add the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append((chunk_text, current_pos, current_pos + len(chunk_text)))

        return chunks


def split_markdown_content(content: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Split markdown content while preserving structural elements.
    """
    splitter = TextSplitter(chunk_size, chunk_overlap)

    # Try to split by headers first to maintain document structure
    header_splits = re.split(r'(\n#{1,6}\s)', content)

    if len(header_splits) > 1:
        # We have headers, process each section separately
        chunks = []
        i = 0
        while i < len(header_splits):
            if header_splits[i].startswith('\n#'):
                # This is a header
                header = header_splits[i]
                if i + 1 < len(header_splits):
                    # Get the content after the header
                    content_after_header = header_splits[i + 1]
                    # Combine header with its content
                    section = header + content_after_header
                    section_chunks = splitter.split_text(section)
                    chunks.extend([chunk[0] for chunk in section_chunks])
                i += 2
            else:
                # This is content without a header
                section_chunks = splitter.split_text(header_splits[i])
                chunks.extend([chunk[0] for chunk in section_chunks])
                i += 1
        return chunks
    else:
        # No headers found, just split the content
        chunks = splitter.split_text(content)
        return [chunk[0] for chunk in chunks]