from typing import List
from src.shared.logger import setup_logger

logger = setup_logger(__name__)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Splits text into context-aware segments.

    Args:
        text (str): The input text to chunk.
        chunk_size (int): The desired size of each chunk.
        overlap (int): The number of characters to overlap between chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    
    # =================================================================================================
    # TODO: HACKATHON CHALLENGE (Pillar 1: Completeness)
    #
    # The current chunking logic is a basic, fixed-size sliding window. This is inefficient and
    # often splits sentences or paragraphs in awkward places, leading to poor context for the LLM.
    #
    # Your challenge is to replace this naive implementation with a more intelligent chunking strategy.
    #
    # REQUIREMENT: You must implement ONE of the following advanced chunking methods:
    #
    #   1. RECURSIVE CHUNKING:
    #      - Split the text recursively by a list of separators (e.g., "\n\n", "\n", " ", "").
    #      - This method tries to keep paragraphs, sentences, and words together as long as possible.
    #      - HINT: Look at how libraries like LangChain implement `RecursiveCharacterTextSplitter`.
    #
    #   2. SEMANTIC CHUNKING:
    #      - Use a sentence embedding model (like `text-embedding-004`) to measure the semantic
    #        similarity between consecutive sentences.
    #      - Split the text where the similarity score drops, indicating a change in topic.
    #      - This is the most advanced method and will likely yield the best RAG performance.
    #      - HINT: You'll need to calculate cosine similarity between sentence embeddings.
    #
    # =================================================================================================

    # Naive, fixed-size chunking (TO BE REPLACED)
    if overlap >= chunk_size:
        logger.warning("Overlap is greater than or equal to chunk_size. Adjusting overlap to be chunk_size - 1.")
        overlap = chunk_size - 1

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)

    logger.info(f"Chunked text into {len(chunks)} segments with chunk_size={chunk_size} and overlap={overlap}.")
    return chunks
