from PyPDF2 import PdfReader
import re

def extract_formatted_text(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""
    
    for page in reader.pages:
        text = page.extract_text()
        
        # Basic formatting improvements
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Try to detect and preserve paragraph breaks
        text = re.sub(r'([.!?])\s', r'\1\n\n', text)
        
        # Remove header/footer page numbers (optional)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        full_text += text + "\n\n"
    
    return full_text

text = extract_formatted_text("{{ pdf_path }}")
text