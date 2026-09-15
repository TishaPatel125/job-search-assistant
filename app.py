import streamlit as st
import os
import json
import tempfile
import streamlit.components.v1 as components
from dotenv import load_dotenv

# Set up page config
st.set_page_config(page_title="Job Search Assistant", page_icon="💼", layout="wide")

# Load environment variables
load_dotenv()

# Check for API keys
if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("TAVILY_API_KEY"):
    st.error("⚠️ Missing API Keys! Please ensure your `.env` file contains OPENROUTER_API_KEY and TAVILY_API_KEY.")
    st.stop()

# Import project modules
try:
    from src.config import ANALYSIS_DIR, RESUME_DIR
    from src.schemas import MarketAnalysis, Resume, GapAnalysis
    from src.phase1.extract_job import process_job_pdf
    from src.phase1.research_company import research_company
    from src.phase3.legitimacy import assess_legitimacy
    from src.phase3.fit_scoring import assess_fit
    from src.phase3.application import generate_application_report
except ImportError as e:
    st.error(f"Error importing modules: {e}. Make sure you are running this from the project root.")
    st.stop()

# App Header
st.title("💼 AI Job Search Assistant")
st.markdown("Analyze the job market, triage your resume gaps, and generate customized application strategies.")

# Load existing data
@st.cache_data
def load_data():
    market_file = os.path.join(ANALYSIS_DIR, 'market-analysis.json')
    resume_file = os.path.join(RESUME_DIR, 'resume.json')
    gap_file = os.path.join(ANALYSIS_DIR, 'gap-analysis.json')
    
    data = {"market": None, "resume": None, "gap": None}
    
    if os.path.exists(market_file):
        with open(market_file, 'r', encoding='utf-8') as f:
            data["market"] = MarketAnalysis(**json.load(f))
    if os.path.exists(resume_file):
        with open(resume_file, 'r', encoding='utf-8') as f:
            data["resume"] = Resume(**json.load(f))
    if os.path.exists(gap_file):
        with open(gap_file, 'r', encoding='utf-8') as f:
            data["gap"] = GapAnalysis(**json.load(f))
            
    return data

data = load_data()

# Layout
tab1, tab2, tab3 = st.tabs(["🚀 Application Advisor", "📊 Market Analysis", "📄 Gap Analysis"])

with tab2:
    if data["market"]:
        st.header("Market Analysis")
        market = data["market"]
        st.metric("Total Postings Analyzed", market.total_postings_analyzed)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Common Skills")
            for skill in market.most_common_skills:
                st.write(f"- {skill}")
        with col2:
            st.subheader("Salary Ranges")
            for sr in market.salary_ranges:
                st.write(f"- {sr}")
    else:
        st.info("No Market Analysis found. Run Phase 1 CLI tool first.")

with tab3:
    if data["gap"]:
        st.header("Resume Gap Analysis")
        gap = data["gap"]
        st.subheader("Your Strengths")
        for s in gap.strengths:
            st.write(f"✅ {s}")
            
        st.subheader("Actionable Gaps")
        for g in gap.gaps:
            with st.expander(f"{g.skill} ({g.level})"):
                st.write(f"**Issue:** {g.description}")
                st.write(f"**Action:** {g.action}")
    else:
        st.info("No Gap Analysis found. Run Phase 2 CLI tool first.")

with tab1:
    st.header("Generate Application Strategy")
    st.write("Upload a new job posting PDF to get a comprehensive fit score, cover letter guide, and interview prep.")
    
    if not data["market"] or not data["resume"] or not data["gap"]:
        st.warning("⚠️ You must complete Phase 1 & 2 before using the Application Advisor.")
    else:
        uploaded_file = st.file_uploader("Upload Job Posting (PDF)", type=["pdf"])
        
        if uploaded_file is not None:
            if st.button("Generate Strategy"):
                with st.status("Analyzing Posting...", expanded=True) as status:
                    # Save temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    
                    try:
                        st.write("📄 Extracting data from PDF...")
                        _, posting = process_job_pdf(tmp_path)
                        
                        st.write("🔍 Researching company...")
                        posting.company_research = research_company(posting.company_name)
                        
                        st.write("🛡️ Assessing posting legitimacy...")
                        legitimacy = assess_legitimacy(posting, data["market"])
                        
                        st.write("🎯 Calculating fit score...")
                        fit = assess_fit(posting, data["resume"], data["market"])
                        
                        st.write("📝 Generating final report...")
                        generate_application_report(posting, data["resume"], data["market"], data["gap"], legitimacy, fit)
                        
                        status.update(label="Analysis Complete!", state="complete", expanded=False)
                        
                        # Display HTML report
                        st.success("Report generated successfully!")
                        html_path = os.path.join("reports", "application-report.html")
                        if os.path.exists(html_path):
                            with open(html_path, 'r', encoding='utf-8') as f:
                                html_content = f.read()
                            st.components.v1.html(html_content, height=800, scrolling=True)
                        
                    except Exception as e:
                        status.update(label="An error occurred", state="error")
                        st.error(f"Error: {str(e)}")
                    finally:
                        os.unlink(tmp_path)
