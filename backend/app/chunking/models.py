from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from app.document.models import DocumentType


@dataclass(slots=True)
class ChunkMetadata:
    """
    Metadata inherited from the parent document.

    Additional metadata can be attached by future
    milestones without modifying the Chunk model.
    """

    page_number: int | None = None

    section: str | None = None

    source: str | None = None

    custom_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Chunk:
    """
    Canonical representation of a semantic chunk.

    Every downstream subsystem (Embeddings,
    Retrieval, Vector DB, RAG) should consume
    this model.
    """

    chunk_id: str

    document_id: str

    document_type: DocumentType

    chunk_index: int

    content: str

    metadata: ChunkMetadata

    start_char: int

    end_char: int

    embedding_id: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )


@dataclass(slots=True)
class ChunkingResult:
    """
    Result produced by a chunking strategy.
    """

    document_id: str

    strategy_name: str

    chunks: list[Chunk]

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    @property
    def total_chunks(self) -> int:
        return len(self.chunks)