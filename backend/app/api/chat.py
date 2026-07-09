from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()


@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):

    conversation_id, response = await chat_service.chat(
        message=request.message,
        conversation_id=request.conversation_id,
    )

    return ChatResponse(
        conversation_id=conversation_id,
        response=response,
    )