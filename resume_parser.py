from pypdf import PdfReader
from docx import Document
from pathlib import Path


def extract_resume_text(file_path):
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(str(file_path))
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text.strip()

    elif extension == ".docx":
        document = Document(str(file_path))
        text = "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

        return text.strip()

    else:
        raise ValueError("Only PDF and DOCX files are supported.")