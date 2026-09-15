import logging
from src.config import DEFAULT_MODEL
from src.llm import get_client
from src.schemas import CompanyResearch
from src.tools.web_search import search

logger = logging.getLogger(__name__)

def research_company(company_name: str) -> CompanyResearch:
    """Research a company using web search and LLM summarization."""
    logger.debug(f'Researching company: {company_name}')
    
    # Perform multiple searches
    queries = [
        f'{company_name} company overview size industry',
        f'{company_name} engineering culture reviews glassdoor',
        f'{company_name} recent news layoffs hiring 2025 2026',
    ]
    
    all_results = []
    for query in queries:
        results = search(query, max_results=3)
        all_results.extend(results)
    
    if not all_results:
        logger.warning(f'No search results found for {company_name}')
        return CompanyResearch(summary=f'No information found for {company_name}')
    
    # Combine search results into context
    context = '\n\n'.join([
        f"Title: {r.get('title', 'N/A')}\nURL: {r.get('url', 'N/A')}\nContent: {r.get('content', 'N/A')}"
        for r in all_results
    ])
    
    # Use LLM to summarize
    client = get_client()
    research = client.chat.completions.create(
        model=DEFAULT_MODEL,
        response_model=CompanyResearch,
        messages=[
            {
                'role': 'system',
                'content': 'You are a company research analyst. Summarize the search results about this company into structured data. Focus on information useful for a job applicant.'
            },
            {
                'role': 'user',
                'content': f'Summarize this research about {company_name}:\n\n{context}'
            }
        ],
        temperature=0.1
    )
    
    logger.debug(f'Company research complete: {company_name} - {research.industry}')
    return research
