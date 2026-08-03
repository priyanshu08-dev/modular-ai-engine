from fastapi import APIRouter, HTTPException, status

from app.retrieval.exceptions import RetrievalError
from app.schemas.retrieval import (
    RetrievalRequestSchema,
    RetrievalResponse,
    RetrievedChunkResponse,
)
from app.services.retrieval_service import RetrievalService

router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)

retrieval_service = RetrievalService()


@router.post(
    "/search",
    response_model=RetrievalResponse,
    status_code=status.HTTP_200_OK,
)
async def search_knowledge(
    request: RetrievalRequestSchema,
):
    """
    Performs semantic similarity search over stored document vectors.
    """
    try:
        result = await retrieval_service.search(
            query=request.query,
            top_k=request.top_k,
            score_threshold=request.score_threshold,
            document_id=request.document_id,
        )

        return RetrievalResponse(
            query=result.query,
            total_results=result.total_results,
            strategy_name=result.strategy_name,
            chunks=[
                RetrievedChunkResponse(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    content=chunk.content,
                    score=chunk.score,
                    metadata=chunk.metadata,
                )
                for chunk in result.chunks
            ],
        )

    except RetrievalError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
