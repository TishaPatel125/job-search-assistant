"""Phase 1: Job Market Analysis CLI

Usage:
    python analyze_market.py --jobs-dir <path-to-pdf-folder> [--verbose] [--force]
"""
import argparse
import logging
import os
import sys
from pathlib import Path

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import setup_logging, validate_env
from src.phase1.extract_job import process_job_pdf
from src.phase1.research_company import research_company
from src.phase1.market_analysis import load_all_jobs, run_market_analysis
from src.config import JOBS_DIR

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Phase 1: Job Market Analysis')
    parser.add_argument('--jobs-dir', required=True, help='Path to directory containing job posting PDFs')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose debug logging')
    parser.add_argument('--force', action='store_true', help='Force re-extraction of all postings')
    args = parser.parse_args()
    
    setup_logging(verbose=args.verbose)
    validate_env()
    
    jobs_dir = args.jobs_dir
    if not os.path.isdir(jobs_dir):
        print(f'Error: {jobs_dir} is not a valid directory')
        sys.exit(1)
    
    # Find all PDFs
    pdfs = sorted([os.path.join(jobs_dir, f) for f in os.listdir(jobs_dir) if f.lower().endswith('.pdf')])
    if not pdfs:
        print(f'Error: No PDF files found in {jobs_dir}')
        sys.exit(1)
    
    print(f'Found {len(pdfs)} job posting PDFs')
    
    # Process each PDF
    all_postings = []
    for i, pdf_path in enumerate(pdfs, 1):
        print(f'\n[{i}/{len(pdfs)}] Processing: {os.path.basename(pdf_path)}')
        try:
            json_path, posting = process_job_pdf(pdf_path, force=args.force)
            
            # Research company if not already done
            if posting.company_research is None or args.force:
                print(f'  Researching company: {posting.company_name}...')
                try:
                    posting.company_research = research_company(posting.company_name)
                    # Update the JSON file with research
                    import json
                    with open(json_path, 'w') as f:
                        f.write(posting.model_dump_json(indent=2))
                except Exception as e:
                    logger.warning(f'Company research failed for {posting.company_name}: {e}')
                    print(f'  Warning: Company research failed (continuing without it)')
            
            all_postings.append(posting)
            print(f'  ✅ {posting.job_title} at {posting.company_name}')
        except Exception as e:
            logger.error(f'Failed to process {pdf_path}: {e}')
            print(f'  ❌ Failed: {e}')
    
    if not all_postings:
        print('\nError: No postings were successfully processed')
        sys.exit(1)
    
    # Generate market analysis
    print(f'\n--- Generating Market Analysis ({len(all_postings)} postings) ---')
    run_market_analysis(all_postings)
    print('\n✅ Market analysis complete!')
    print('  📊 JSON: data/analysis/market-analysis.json')
    print('  📝 Report: reports/market-analysis.md')

if __name__ == '__main__':
    main()
