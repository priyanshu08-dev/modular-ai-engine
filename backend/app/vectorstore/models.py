from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class VectorRecord:
    """
    Represents one vector ready to be stored
    inside the configured vector database.
    """

    embedding_id: str

    chunk_id: str

    document_id: str

    content: str

    vector: list[float]

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class VectorBatch:
    """
    Represents an entire document worth of vectors.
    """

    document_id: str

    vectors: list[VectorRecord]