from typing import Any

from pydantic import BaseModel, Field


class RetrievalRequestSchema(BaseModel):
    query: str = Field(..., description="User query text for semantic search.")
    top_k: int = Field(5, ge=1, le=50, description="Maximum number of relevant chunks to retrieve.")
    score_threshold: float = Field(0.0, ge=0.0, le=1.0, description="Minimum similarity score cutoff threshold.")
    document_id: str | None = Field(None, description="Optional document ID to restrict search scope.")


class RetrievedChunkResponse(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: dict[str, Any]


class RetrievalResponse(BaseModel):
    query: str
    total_results: int
    strategy_name: str
    chunks: list[RetrievedChunkResponse]
