from src.search.vertex_client import VertexSearchClient
from src.shared.logger import setup_logger

logger = setup_logger(__name__)

def search_knowledge_base(query: str) -> str:
    """
    Searches the knowledge base using the VertexSearchClient.

    Args:
        query (str): The search query.

    Returns:
        str: Consolidated context from retrieved documents.
    """
    logger.info(f"Tool call: search_knowledge_base with query: {query}")
    vertex_search_client = VertexSearchClient()
    return vertex_search_client.search(query)
