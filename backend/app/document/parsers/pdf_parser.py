from pathlib import Path

from pypdf import PdfReader

from app.document.models import DocumentType
from app.document.parsers.base import BaseDocumentParser


class PDFParser(BaseDocumentParser):
    DOCUMENT_TYPE = DocumentType.PDF
    MIME_TYPE = "application/pdf"

    def load(self, file_path: Path) -> PdfReader:
        return PdfReader(file_path)

    def extract_text(self, document: PdfReader) -> str:
        return "\n".join(page.extract_text() or "" for page in document.pages)

    def get_page_count(self, document: PdfReader) -> int:
        return len(document.pages)
