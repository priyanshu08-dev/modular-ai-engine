from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: str | None = Field(
        None, description="Optional conversation UUID for multi-turn chat."
    )
    message: str = Field(..., description="User chat query.")
    enable_rag: bool = Field(
        True, description="Enable Retrieval-Augmented Generation using uploaded documents."
    )
    document_id: str | None = Field(
        None, description="Optional document ID filter to scope RAG search."
    )
    top_k: int | None = Field(
        None, ge=1, le=20, description="Max context chunks to retrieve for RAG."
    )
    score_threshold: float | None = Field(
        None, ge=0.0, le=1.0, description="Similarity score cutoff threshold for RAG chunks."
    )
