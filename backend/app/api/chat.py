import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()


@router.post("/")
async def chat(
    request: ChatRequest,
):
    """
    Conversational endpoint streaming token responses using Server-Sent Events (SSE).
    Returns conversation metadata and retrieved RAG sources in initial SSE event.
    """
    conversation_id, stream, context = await chat_service.stream_chat(
        message=request.message,
        conversation_id=request.conversation_id,
        enable_rag=request.enable_rag,
        document_id=request.document_id,
        top_k=request.top_k,
        score_threshold=request.score_threshold,
    )

    async def response_stream():
        metadata_payload = {
            "conversation_id": conversation_id,
            "rag_enabled": context.metadata.get("rag_enabled", False),
            "sources": context.metadata.get("sources", []),
        }

        yield (
            "event: metadata\n"
            f"data: {json.dumps(metadata_payload)}\n\n"
        )

        if stream:
            async for chunk in stream:
                yield (
                    "event: token\n"
                    f"data: {json.dumps(chunk)}\n\n"
                )

        yield (
            "event: done\n"
            "data: {}\n\n"
        )

    return StreamingResponse(
        response_stream(),
        media_type="text/event-stream",
    )