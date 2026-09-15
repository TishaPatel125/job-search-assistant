import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import argparse
import os
import json
import logging
from src.config import setup_logging, validate_env, ANALYSIS_DIR, RESUME_DIR
from src.schemas import MarketAnalysis, Resume, GapAnalysis
from src.phase1.extract_job import process_job_pdf
from src.phase1.research_company import research_company
from src.phase3.legitimacy import assess_legitimacy
from src.phase3.fit_scoring import assess_fit
from src.phase3.application import generate_application_report

def main():
    parser = argparse.ArgumentParser(description="Application Advisor")
    parser.add_argument("posting", help="Path to the new job posting PDF")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    validate_env()
    
    market_file = os.path.join(ANALYSIS_DIR, 'market-analysis.json')
    resume_file = os.path.join(RESUME_DIR, 'resume.json')
    gap_file = os.path.join(ANALYSIS_DIR, 'gap-analysis.json')
    
    for f_path in [market_file, resume_file, gap_file]:
        if not os.path.exists(f_path):
            logging.error(f"Required file {f_path} not found. Run previous phases.")
            sys.exit(1)
            
    with open(market_file, 'r', encoding='utf-8') as f:
        market = MarketAnalysis(**json.load(f))
    with open(resume_file, 'r', encoding='utf-8') as f:
        resume = Resume(**json.load(f))
    with open(gap_file, 'r', encoding='utf-8') as f:
        gap_analysis = GapAnalysis(**json.load(f))
        
    logging.info("Extracting new job posting...")
    _, posting = process_job_pdf(args.posting)
    
    logging.info("Researching company...")
    posting.company_research = research_company(posting.company_name)
    
    logging.info("Assessing legitimacy...")
    legitimacy = assess_legitimacy(posting, market)
    
    logging.info("Assessing fit...")
    fit = assess_fit(posting, resume, market)
    
    logging.info("Generating report...")
    generate_application_report(posting, resume, market, gap_analysis, legitimacy, fit)
    
    print("Application advice generated successfully. Check reports/application-report.html")

if __name__ == "__main__":
    main()
