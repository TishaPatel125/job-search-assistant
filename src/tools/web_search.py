import logging
import os
from tavily import TavilyClient

logger = logging.getLogger(__name__)

def search(query: str, max_results: int = 5) -> list[dict]:
    """Perform a web search using Tavily API."""
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        logger.error('TAVILY_API_KEY not found')
        return []
    
    logger.debug(f'Tool call: web_search("{query}")')
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=max_results, search_depth='basic')
        results = response.get('results', [])
        logger.debug(f'Search returned {len(results)} results')
        for r in results[:3]:
            logger.debug(f'  - {r.get("title", "No title")}: {r.get("url", "")}')
        return results
    except Exception as e:
        logger.error(f'Web search failed: {e}')
        return []
