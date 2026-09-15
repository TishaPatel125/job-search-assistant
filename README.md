# Assignment 2: Job Search Assistant

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file in the root of the project with:
   ```env
   OPENROUTER_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   ```

## Running the Application

### Phase 1: Job Market Analysis
Extracts data from job posting PDFs, researches companies, and produces a market analysis.
```bash
python analyze_market.py --jobs-dir "sample-data/jobs" --verbose
```
Outputs are saved to `data/jobs/`, `data/analysis/market-analysis.json`, and `reports/market-analysis.md`.

### Phase 2: Resume Gap Analysis
Analyzes your resume against the market data and triages gaps.
```bash
python analyze_resume.py --resume "sample-data/resume.pdf" --verbose
```
Outputs are saved to `data/resume/resume.json`, `data/analysis/gap-analysis.json`, and `reports/gap-analysis.md`.

### Phase 3: Application Advisor
Assesses a new job posting for legitimacy and fit, providing a comprehensive HTML report.
```bash
python advise.py "sample-data/jobs/fullstack-dev-wealthsimple.pdf" --verbose
```
Output is saved to `reports/application-report.html`.

## Evaluation
See the `eval/` directory for manual evaluation checks, and `docs/reflection.md` for project reflections.
