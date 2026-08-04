from langchain_core.messages import HumanMessage

from app.engine.execution_context import ExecutionContext
from app.engine.memory import memory_manager
from app.engine.pipeline import ExecutionPipeline
from app.engine.pipeline.steps import (
    MemoryStep,
    ProviderStep,
    RAGStep,
)


class AIEngine:
    """
    Central orchestration layer for AI execution.
    """

    def __init__(self) -> None:
        self.pipeline = ExecutionPipeline(
            [
                MemoryStep(memory_manager),
                RAGStep(),
                ProviderStep(memory_manager),
            ]
        )

    async def stream(
        self,
        message: str,
        conversation_id: str | None = None,
        enable_rag: bool = True,
        document_id: str | None = None,
        top_k: int | None = None,
        score_threshold: float | None = None,
    ) -> tuple[str, object, ExecutionContext]:
        """
        Executes the AI execution pipeline in streaming mode.
        Returns conversation_id, token stream, and updated ExecutionContext.
        """
        context = ExecutionContext(
            conversation_id=conversation_id or "",
            input_message=HumanMessage(content=message),
            metadata={
                "enable_rag": enable_rag,
                "document_id": document_id,
                "top_k": top_k,
                "score_threshold": score_threshold,
            },
        )

        context = await self.pipeline.stream(context)

        return (
            context.conversation_id,
            context.stream,
            context,
        )

    async def run(
        self,
        message: str,
        conversation_id: str | None = None,
        enable_rag: bool = True,
        document_id: str | None = None,
        top_k: int | None = None,
        score_threshold: float | None = None,
    ) -> tuple[str, str, ExecutionContext]:
        """
        Executes the pipeline synchronously.
        """
        conversation_id, stream, context = await self.stream(
            message=message,
            conversation_id=conversation_id,
            enable_rag=enable_rag,
            document_id=document_id,
            top_k=top_k,
            score_threshold=score_threshold,
        )

        chunks: list[str] = []

        if stream:
            async for chunk in stream:  # type: ignore[union-attr]
                chunks.append(chunk)

        response_text = "".join(chunks)
        context.response = response_text

        return (
            conversation_id,
            response_text,
            context,
        )
