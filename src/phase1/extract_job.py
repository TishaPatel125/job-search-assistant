import json
import logging
import os
from datetime import datetime
from pathlib import Path

from src.config import JOBS_DIR, DEFAULT_MODEL
from src.llm import get_client
from src.pdf_extractor import extract_text_from_pdf
from src.schemas import JobPosting

logger = logging.getLogger(__name__)

def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:60]

def extract_job_posting(pdf_path: str) -> JobPosting:
    """Extract structured job posting data from a PDF."""
    logger.debug(f'Extracting posting: {os.path.basename(pdf_path)}')
    
    text = extract_text_from_pdf(pdf_path)
    if not text:
        raise ValueError(f'No text could be extracted from {pdf_path}')
    
    today = datetime.now().strftime('%Y-%m-%d')
    client = get_client()
    
    posting = client.chat.completions.create(
        model=DEFAULT_MODEL,
        response_model=JobPosting,
        messages=[
            {
                'role': 'system',
                'content': f"""You are a job posting data extractor. Extract structured data from the job posting text provided.

Today's date is {today}. Use this to calculate posting_age_days from any date information in the posting.
If the posting says "Posted X days ago", use that directly as posting_age_days.
If no date information is present, set posting_age_days to null.

For fields not present in the posting, use null rather than guessing.
Be thorough in extracting ALL required and preferred skills mentioned.
For remote_status, use one of: 'remote', 'hybrid', 'onsite', or 'not listed'."""
            },
            {
                'role': 'user',
                'content': f'Extract structured data from this job posting:\n\n{text}'
            }
        ],
        temperature=0.1
    )
    
    posting.source_file = os.path.basename(pdf_path)
    
    logger.debug(f'Extracted {len(posting.required_skills)} required skills, {len(posting.preferred_skills)} preferred skills')
    logger.debug(f'Salary field: {posting.salary_range or "not found in posting"}')
    logger.debug(f'posting_age_days: {posting.posting_age_days}')
    
    return posting

def process_job_pdf(pdf_path: str, force: bool = False) -> tuple[str, JobPosting]:
    """Process a single job PDF. Returns (json_path, posting). Skips if already processed."""
    # Determine output path based on PDF filename
    pdf_name = Path(pdf_path).stem
    json_filename = f'{slugify(pdf_name)}.json'
    json_path = os.path.join(JOBS_DIR, json_filename)
    
    # Skip if already processed
    if os.path.exists(json_path) and not force:
        logger.info(f'Skipping {os.path.basename(pdf_path)} (already processed)')
        with open(json_path, 'r') as f:
            posting = JobPosting.model_validate_json(f.read())
        return json_path, posting
    
    # Extract and save
    posting = extract_job_posting(pdf_path)
    
    os.makedirs(JOBS_DIR, exist_ok=True)
    with open(json_path, 'w') as f:
        f.write(posting.model_dump_json(indent=2))
    
    logger.info(f'Saved extraction to {json_path}')
    return json_path, posting
