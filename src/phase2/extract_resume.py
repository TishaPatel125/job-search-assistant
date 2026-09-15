import os
import json
import logging
from src.schemas import Resume
from src.pdf_extractor import extract_text_from_pdf
from src.llm import get_client
from src.config import RESUME_DIR, DEFAULT_MODEL

logger = logging.getLogger(__name__)

def extract_resume(pdf_path: str) -> Resume:
    logger.info(f"Extracting resume from {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    client = get_client()
    
    resume = client.chat.completions.create(
        model=DEFAULT_MODEL,
        response_model=Resume,
        messages=[
            {"role": "system", "content": "You are a professional resume parser. Extract the resume details into the provided schema. Be accurate and concise."},
            {"role": "user", "content": f"Resume Text:\n{text}"}
        ]
    )
    
    output_path = os.path.join(RESUME_DIR, 'resume.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(resume.model_dump_json(indent=2))
        
    logger.info(f"Saved extracted resume to {output_path}")
    return resume
