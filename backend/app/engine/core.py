from app.engine.execution_context import ExecutionContext
from app.engine.pipeline import ExecutionPipeline
from app.engine.pipeline.steps import (
    MemoryStep,
    ProviderStep,
)
from app.engine.memory import memory_manager
from langchain_core.messages import HumanMessage


class AIEngine:
    """
    Central orchestration layer for AI execution.
    """

    def __init__(self):

        self.pipeline = ExecutionPipeline(
            [
                MemoryStep(memory_manager),
                ProviderStep(memory_manager),
            ]
        )

    async def stream(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> tuple[str, object]:

        context = ExecutionContext(
            conversation_id=conversation_id or "",
            input_message=HumanMessage(content=message),
        )

        context = await self.pipeline.stream(context)

        return (
            context.conversation_id,
            context.stream,
        )

    async def run(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> tuple[str, str]:

        conversation_id, stream = await self.stream(
            message=message,
            conversation_id=conversation_id,
        )

        chunks: list[str] = []

        async for chunk in stream:
            chunks.append(chunk)

        return (
            conversation_id,
            "".join(chunks),
        )