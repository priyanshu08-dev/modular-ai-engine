from app.engine.execution_context import ExecutionContext
from app.engine.pipeline import ExecutionPipeline
from app.engine.pipeline.steps import (
    MemoryStep,
    ProviderStep,
)
from langchain_core.messages import HumanMessage
from app.engine.memory import memory_manager



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

    async def run(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> tuple[str, str]:

        context = ExecutionContext(
            conversation_id=conversation_id or "",
            input_message=HumanMessage(content=message),
        )

        context = await self.pipeline.execute(
            context,
        )

        return (
            context.conversation_id,
            context.response,
        )