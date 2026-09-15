import os
import logging
from src.config import REPORTS_DIR

logger = logging.getLogger(__name__)

def generate_application_report(posting, resume, market, gap_analysis, legitimacy, fit) -> str:
    logger.info("Generating HTML application report")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Application Report: {posting.job_title} at {posting.company_name}</title>
        <style>
            :root {{
                --bg: #121212;
                --surface: #1e1e1e;
                --text: #e0e0e0;
                --primary: #bb86fc;
                --green: #03dac6;
                --red: #cf6679;
                --yellow: #f2c94c;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
            }}
            h1, h2, h3 {{ color: var(--primary); }}
            .card {{
                background: var(--surface);
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }}
            .legitimacy-green {{ border-left: 5px solid var(--green); }}
            .legitimacy-yellow {{ border-left: 5px solid var(--yellow); }}
            .legitimacy-red {{ border-left: 5px solid var(--red); }}
            
            .progress-bg {{
                background: #333;
                border-radius: 10px;
                height: 20px;
                width: 100%;
                margin-top: 10px;
            }}
            .progress-bar {{
                background: var(--primary);
                height: 20px;
                border-radius: 10px;
            }}
            ul {{ padding-left: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Application Advisor: {posting.job_title} @ {posting.company_name}</h1>
            
            <div class="card legitimacy-{legitimacy.verdict.lower()}">
                <h2>1. Legitimacy Assessment: {legitimacy.verdict.upper()}</h2>
                <p><strong>Confidence:</strong> {legitimacy.confidence_score * 100:.1f}%</p>
                <p><strong>Recommendation:</strong> {legitimacy.recommendation}</p>
                <ul>
                    {"".join(f"<li><b>{s.signal_type.upper()}</b> ({s.category}): {s.description} - {s.evidence}</li>" for s in legitimacy.signals)}
                </ul>
            </div>
            
            <div class="card">
                <h2>2. Fit Assessment</h2>
                <p><strong>Overall Score:</strong> {fit.overall_score:.1f}/100</p>
                <div class="progress-bg"><div class="progress-bar" style="width: {fit.overall_score}%"></div></div>
                <p><strong>Recommendation:</strong> {fit.recommendation}</p>
                <h3>Category Breakdowns</h3>
                {"".join(f"<div><h4>{c.category} ({c.score * 100:.1f}%)</h4><p>{c.notes}</p></div>" for c in fit.categories)}
            </div>
            
            <div class="card">
                <h2>3. Resume Adaptation Guidance</h2>
                <ul>
                    {"".join(f"<li>{s}</li>" for s in fit.resume_suggestions)}
                </ul>
            </div>
            
            <div class="card">
                <h2>4. Cover Letter Points</h2>
                <ul>
                    {"".join(f"<li>{p}</li>" for p in fit.cover_letter_points)}
                </ul>
            </div>
            
            <div class="card">
                <h2>5. Interview Preparation</h2>
                <h3>Potential Questions</h3>
                <ul>
                    {"".join(f"<li>{q}</li>" for q in fit.interview_questions)}
                </ul>
                <h3>Skills to Review</h3>
                <ul>
                    {"".join(f"<li>{s}</li>" for s in fit.skills_to_review)}
                </ul>
                <h3>Company Research Points</h3>
                <ul>
                    {"".join(f"<li>{r}</li>" for r in fit.company_research_points)}
                </ul>
                <h3>Talking Points</h3>
                <ul>
                    {"".join(f"<li>{t}</li>" for t in fit.talking_points)}
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    html_path = os.path.join(REPORTS_DIR, 'application-report.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    logger.info(f"Saved application report to {html_path}")
    return html
