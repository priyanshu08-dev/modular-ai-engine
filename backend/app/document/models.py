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
    """
    Standardized representation of a parsed document.

    This model becomes the canonical input for all downstream
    processing pipelines including chunking, embeddings,
    retrieval, and RAG.
    """

    document_id: str

    document_type: DocumentType

    content: str

    metadata: DocumentMetadata
