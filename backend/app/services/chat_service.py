from collections.abc import AsyncIterator

from app.engine import AIEngine
from app.engine.execution_context import ExecutionContext


class ChatService:
    """Application service coordinating chat and RAG execution."""

    def __init__(self) -> None:
        self.engine = AIEngine()

    async def chat(
        self,
        message: str,
        conversation_id: str | None = None,
        enable_rag: bool = True,
        document_id: str | None = None,
        top_k: int | None = None,
        score_threshold: float | None = None,
    ) -> tuple[str, str, ExecutionContext]:
        return await self.engine.run(
            message=message,
            conversation_id=conversation_id,
            enable_rag=enable_rag,
            document_id=document_id,
            top_k=top_k,
            score_threshold=score_threshold,
        )

    async def stream_chat(
        self,
        message: str,
        conversation_id: str | None = None,
        enable_rag: bool = True,
        document_id: str | None = None,
        top_k: int | None = None,
        score_threshold: float | None = None,
    ) -> tuple[str, AsyncIterator[str], ExecutionContext]:
        return await self.engine.stream(
            message=message,
            conversation_id=conversation_id,
            enable_rag=enable_rag,
            document_id=document_id,
            top_k=top_k,
            score_threshold=score_threshold,
        )
