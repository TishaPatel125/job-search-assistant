import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import argparse
import os
import json
import logging
from src.config import setup_logging, validate_env, ANALYSIS_DIR
from src.schemas import MarketAnalysis
from src.phase2.extract_resume import extract_resume
from src.phase2.gap_analysis import run_gap_analysis

def main():
    parser = argparse.ArgumentParser(description="Analyze a resume and generate a gap report.")
    parser.add_argument("--resume", required=True, help="Path to the resume PDF")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    validate_env()
    
    market_file = os.path.join(ANALYSIS_DIR, 'market-analysis.json')
    if not os.path.exists(market_file):
        logging.error(f"Market analysis not found at {market_file}. Run Phase 1 first.")
        sys.exit(1)
        
    with open(market_file, 'r', encoding='utf-8') as f:
        market_data = json.load(f)
        market = MarketAnalysis(**market_data)
        
    resume = extract_resume(args.resume)
    run_gap_analysis(resume, market)
    
    print("Gap analysis completed successfully. Check reports/gap-analysis.md for details.")

if __name__ == "__main__":
    main()
