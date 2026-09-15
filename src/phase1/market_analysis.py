import json
import logging
import os
from src.config import JOBS_DIR, ANALYSIS_DIR, REPORTS_DIR, DEFAULT_MODEL
from src.llm import get_client, get_raw_client
from src.schemas import JobPosting, MarketAnalysis

logger = logging.getLogger(__name__)

def load_all_jobs() -> list[JobPosting]:
    """Load all extracted job postings from JSON files."""
    jobs = []
    if not os.path.exists(JOBS_DIR):
        return jobs
    for filename in sorted(os.listdir(JOBS_DIR)):
        if filename.endswith('.json'):
            filepath = os.path.join(JOBS_DIR, filename)
            with open(filepath, 'r') as f:
                job = JobPosting.model_validate_json(f.read())
                jobs.append(job)
    logger.info(f'Loaded {len(jobs)} job postings')
    return jobs

def generate_market_analysis(jobs: list[JobPosting]) -> MarketAnalysis:
    """Generate aggregated market analysis from job postings."""
    # Prepare summary of all jobs for the LLM
    jobs_summary = json.dumps([j.model_dump(exclude={'company_research'}) for j in jobs], indent=2)
    
    client = get_client()
    analysis = client.chat.completions.create(
        model=DEFAULT_MODEL,
        response_model=MarketAnalysis,
        messages=[
            {
                'role': 'system',
                'content': 'You are a job market analyst. Analyze the following job postings and identify patterns, trends, and common requirements across all postings. Be specific and data-driven in your analysis.'
            },
            {
                'role': 'user',
                'content': f'Analyze these {len(jobs)} job postings and identify market patterns:\n\n{jobs_summary}'
            }
        ],
        temperature=0.1
    )
    analysis.total_postings_analyzed = len(jobs)
    return analysis

def generate_market_report(analysis: MarketAnalysis, jobs: list[JobPosting]) -> str:
    """Generate a human-readable market analysis report."""
    raw_client = get_raw_client()
    
    analysis_json = analysis.model_dump_json(indent=2)
    jobs_summary = json.dumps(
        [{'title': j.job_title, 'company': j.company_name, 'location': j.location, 
          'salary': j.salary_range, 'skills': j.required_skills} for j in jobs],
        indent=2
    )
    
    response = raw_client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                'role': 'system',
                'content': 'You are a job market analyst. Write a detailed, well-formatted Markdown report based on the market analysis data. Include sections for: Overview, Skills & Technologies, Experience & Education, Compensation, Common Responsibilities, Trends & Observations. Use tables, bullet points, and clear formatting.'
            },
            {
                'role': 'user',
                'content': f'Write a market analysis report based on this data:\n\nAnalysis:\n{analysis_json}\n\nJob Postings:\n{jobs_summary}'
            }
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def run_market_analysis(jobs: list[JobPosting]) -> None:
    """Run the full market analysis pipeline and save outputs."""
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    logger.info('Generating market analysis...')
    analysis = generate_market_analysis(jobs)
    
    # Save JSON
    json_path = os.path.join(ANALYSIS_DIR, 'market-analysis.json')
    with open(json_path, 'w') as f:
        f.write(analysis.model_dump_json(indent=2))
    logger.info(f'Saved market analysis to {json_path}')
    
    # Generate and save report
    logger.info('Generating market analysis report...')
    report = generate_market_report(analysis, jobs)
    report_path = os.path.join(REPORTS_DIR, 'market-analysis.md')
    with open(report_path, 'w') as f:
        f.write(report)
    logger.info(f'Saved market analysis report to {report_path}')
