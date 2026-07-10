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

    conversation_id, stream = await chat_service.stream_chat(
        message=request.message,
        conversation_id=request.conversation_id,
    )

    async def response_stream():

        yield (
            "event: metadata\n"
            f"data: {json.dumps({'conversation_id': conversation_id})}\n\n"
        )

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