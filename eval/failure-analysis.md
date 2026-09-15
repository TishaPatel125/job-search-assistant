# Failure Analysis & Overall Observations

### Failure 1: Complex PDF Layouts
- **What happened**: When processing a highly stylized PDF with a complex multi-column layout, PyMuPDF extracted the text out of order.
- **Why it happened**: PyMuPDF reads blocks of text and sometimes misinterprets visual columns as horizontal rows if the PDF isn't tagged properly.
- **Fix**: Switch to a more layout-aware extractor like `pdfplumber` for complex documents, or use a vision-capable LLM to parse the raw PDF image.

### Failure 2: WHOIS Rate Limiting
- **What happened**: During rapid testing, the WHOIS tool started returning connection errors.
- **Why it happened**: WHOIS servers often have strict rate limits and will temporarily block IPs that make too many requests in a short period.
- **Fix**: Implement a caching layer so we don't query the same domain twice, and add exponential backoff/retry logic specifically for the WHOIS socket connection.

### Overall Summary
The system does a fantastic job of taking unstructured PDF text and turning it into highly actionable, structured advice. The structured outputs via Pydantic make the data incredibly reliable. The main shortcoming is the fragility of external tools (Tavily search failures or WHOIS rate limits) and raw PDF text extraction formatting.
