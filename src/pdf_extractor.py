import logging
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from a PDF file using PyMuPDF."""
    logger.debug(f'Extracting text from PDF: {pdf_path}')
    try:
        doc = fitz.open(pdf_path)
        text = ''
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            text += page_text
            logger.debug(f'  Page {page_num + 1}: {len(page_text)} characters')
        doc.close()
        logger.debug(f'Total extracted: {len(text)} characters')
        if not text.strip():
            logger.warning(f'PDF appears to be empty or image-only: {pdf_path}')
        return text.strip()
    except Exception as e:
        logger.error(f'Failed to extract text from {pdf_path}: {e}')
        raise
