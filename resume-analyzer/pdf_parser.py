"""PDF resume text extraction and cleanup."""

from __future__ import annotations

import re
from io import BytesIO

import fitz  # PyMuPDF


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract and clean text from a PDF resume."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages: list[str] = []

    for page in doc:
        text = page.get_text("text")
        if text.strip():
            pages.append(text)

    doc.close()
    raw_text = "\n".join(pages)
    return clean_resume_text(raw_text)


def clean_resume_text(text: str) -> str:
    """Normalize messy PDF formatting into readable plain text."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\f", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?m)^[•●▪◦·]\s*", "- ", text)
    return text.strip()


def extract_text_from_path(file_path: str) -> str:
    """Extract text from a PDF file on disk."""
    with open(file_path, "rb") as f:
        return extract_text_from_pdf(f.read())


def extract_text_from_upload(upload_file) -> str:
    """Extract text from a FastAPI UploadFile."""
    content = upload_file.file.read()
    return extract_text_from_pdf(BytesIO(content).getvalue())
