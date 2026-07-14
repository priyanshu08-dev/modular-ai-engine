from pathlib import Path

from app.document.models import DocumentType
from app.document.parsers.base import BaseDocumentParser


class TXTParser(BaseDocumentParser):
    DOCUMENT_TYPE = DocumentType.TXT
    MIME_TYPE = "text/plain"

    def load(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")

    def extract_text(self, document: str) -> str:
        return document
