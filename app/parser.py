import pdfplumber
from docx import Document

def extract_text(file_bytes: bytes, filename: str) -> str:
    if filename.endswith(".pdf"):
        with pdfplumber.open(file_bytes) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif filename.endswith(".docx"):
        doc = Document(file_bytes)
        return "\n".join(para.text for para in doc.paragraphs)
    raise ValueError("Unsupported file format. Upload PDF or DOCX.")