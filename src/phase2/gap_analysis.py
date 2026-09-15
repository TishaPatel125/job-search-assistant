import os
import logging
from typing import Dict, Any
from src.schemas import Resume, MarketAnalysis, GapAnalysis, SkillGap
from src.llm import get_client
from src.config import ANALYSIS_DIR, REPORTS_DIR, DEFAULT_MODEL
from src.tools.web_search import search

logger = logging.getLogger(__name__)

def run_gap_analysis(resume: Resume, market: MarketAnalysis) -> GapAnalysis:
    logger.info("Running gap analysis")
    
    client = get_client()
    gap_analysis = client.chat.completions.create(
        model=DEFAULT_MODEL,
        response_model=GapAnalysis,
        messages=[
            {"role": "system", "content": "You are an expert career counselor. Compare the candidate's resume with the market analysis. Identify strengths, gaps (quick_win, short_term, medium_term, long_term), and unique value. Be specific."},
            {"role": "user", "content": f"Resume:\n{resume.model_dump_json(indent=2)}\n\nMarket Analysis:\n{market.model_dump_json(indent=2)}"}
        ]
    )
    
    for gap in gap_analysis.gaps:
        logger.info(f"Finding actionable recommendations for gap: {gap.skill}")
        query = f"how to learn {gap.skill} fast course certification"
        results = search(query, max_results=3)
        links = "\n".join([f"- {r.get('title')}: {r.get('url')}" for r in results])
        gap.action += f"\n\nResources found:\n{links}"
        
    json_path = os.path.join(ANALYSIS_DIR, 'gap-analysis.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(gap_analysis.model_dump_json(indent=2))
    logger.info(f"Saved gap analysis JSON to {json_path}")
        
    md_path = os.path.join(REPORTS_DIR, 'gap-analysis.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Gap Analysis Report\n\n")
        f.write("## Strengths\n")
        for s in gap_analysis.strengths:
            f.write(f"- {s}\n")
        f.write("\n## Skill Gaps\n")
        for g in gap_analysis.gaps:
            f.write(f"### {g.skill} ({g.level})\n")
            f.write(f"**Description**: {g.description}\n")
            f.write(f"**Action Plan**: {g.action}\n\n")
        f.write("## Unique Value Proposition\n")
        for u in gap_analysis.unique_value:
            f.write(f"- {u}\n")
            
    logger.info(f"Saved gap analysis report to {md_path}")
    return gap_analysis
