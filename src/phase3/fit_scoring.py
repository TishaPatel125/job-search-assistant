import logging
from src.schemas import JobPosting, Resume, MarketAnalysis, FitAssessment
from src.llm import get_client
from src.config import DEFAULT_MODEL

logger = logging.getLogger(__name__)

def assess_fit(posting: JobPosting, resume: Resume, market: MarketAnalysis) -> FitAssessment:
    logger.info("Assessing candidate fit for the job posting")
    
    client = get_client()
    assessment = client.chat.completions.create(
        model=DEFAULT_MODEL,
        response_model=FitAssessment,
        messages=[
            {"role": "system", "content": "You are an encouraging career coach. Assess the candidate's fit for the job. NEVER say 'don't apply' or be overly negative. Always focus on how to position their existing skills and what to quickly learn."},
            {"role": "user", "content": f"Job Posting:\n{posting.model_dump_json(indent=2)}\n\nResume:\n{resume.model_dump_json(indent=2)}\n\nMarket Context:\n{market.model_dump_json(indent=2)}"}
        ]
    )
    
    return assessment
