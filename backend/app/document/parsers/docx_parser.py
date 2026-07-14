from pathlib import Path

from docx import Document as DocxDocument

from app.document.models import DocumentType
from app.document.parsers.base import BaseDocumentParser


class DOCXParser(BaseDocumentParser):
    DOCUMENT_TYPE = DocumentType.DOCX
    MIME_TYPE = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    def load(self, file_path: Path) -> DocxDocument:
        return DocxDocument(file_path)

    def extract_text(self, document: DocxDocument) -> str:
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
