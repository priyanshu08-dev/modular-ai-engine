from dataclasses import dataclass
from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MARKDOWN = "md"


@dataclass(slots=True)
class DocumentMetadata:
    filename: str
    extension: str
    mime_type: str
    size: int
    page_count: int | None = None
    character_count: int = 0
    word_count: int = 0


@dataclass(slots=True)
class Document:
    document_type: DocumentType
    content: str
    metadata: DocumentMetadata
