from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True, frozen=True)
class EmbeddingMetadata:
    """
    Metadata associated with a generated embedding.
    """

    provider: str
    model: str
    dimensions: int
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    additional_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Embedding:
    """
    Represents the embedding generated for a single document chunk.
    """

    embedding_id: str
    chunk_id: str
    vector: Sequence[float]
    metadata: EmbeddingMetadata


@dataclass(slots=True)
class EmbeddingResult:
    """
    Represents the complete embedding output for a document.
    """

    document_id: str
    embeddings: list[Embedding]
