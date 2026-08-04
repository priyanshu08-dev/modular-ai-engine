from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True, frozen=True)
class SourceAttribution:
    """
    Represents metadata and content snippets of a document chunk
    used to ground an AI response.
    """

    document_id: str
    chunk_id: str
    score: float
    content_snippet: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RAGContext:
    """
    Container for formatted context text and structured source attributions
    generated from retrieved knowledge chunks.
    """

    query: str
    formatted_context: str
    sources: list[SourceAttribution]
    total_sources: int
    has_relevant_context: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
