import os
import sys
import logging
from dotenv import load_dotenv, find_dotenv

# Define Path Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
JOBS_DIR = os.path.join(DATA_DIR, 'jobs')
RESUME_DIR = os.path.join(DATA_DIR, 'resume')
ANALYSIS_DIR = os.path.join(DATA_DIR, 'analysis')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
EVAL_DIR = os.path.join(BASE_DIR, 'eval')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# Create directories
for d in [DATA_DIR, JOBS_DIR, RESUME_DIR, ANALYSIS_DIR, REPORTS_DIR, EVAL_DIR, DOCS_DIR]:
    os.makedirs(d, exist_ok=True)

DEFAULT_MODEL = 'google/gemini-2.5-flash'

def load_environment():
    load_dotenv(find_dotenv())

def validate_env():
    load_environment()
    required = ['OPENROUTER_API_KEY', 'TAVILY_API_KEY']
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

def setup_logging(verbose=False):
    log_level = logging.DEBUG if verbose or '--verbose' in sys.argv or '--debug' in sys.argv or os.getenv('LOG_LEVEL') == 'DEBUG' else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]
    )
