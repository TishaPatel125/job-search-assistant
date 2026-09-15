import logging
from urllib.parse import urlparse
from src.schemas import JobPosting, MarketAnalysis, LegitimacyAssessment
from src.tools.whois_lookup import lookup
from src.tools.web_search import search
from src.llm import get_client
from src.config import DEFAULT_MODEL

logger = logging.getLogger(__name__)

def assess_legitimacy(posting: JobPosting, market: MarketAnalysis) -> LegitimacyAssessment:
    logger.info("Assessing job posting legitimacy")
    
    company = posting.company_name
    query = f"{company} official website"
    search_results = search(query, max_results=2)
    
    domain = None
    if search_results:
        url = search_results[0].get('url', '')
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        
    whois_info = None
    if domain:
        whois_info = lookup(domain)
        
    context = {
        "job_posting": posting.model_dump(),
        "market_analysis": market.model_dump(),
        "domain_found": domain,
        "whois_info": whois_info.model_dump() if whois_info else None,
        "search_results": search_results
    }
    
    client = get_client()
    assessment = client.chat.completions.create(
        model=DEFAULT_MODEL,
        response_model=LegitimacyAssessment,
        messages=[
            {"role": "system", "content": "You are a cybersecurity and job market expert. Assess the legitimacy of this job posting. Look for red flags like unusually high salary, recent domain registration, sketchy web presence, etc."},
            {"role": "user", "content": f"Context data:\n{context}"}
        ]
    )
    
    return assessment
