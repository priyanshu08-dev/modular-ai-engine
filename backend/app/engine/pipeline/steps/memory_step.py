from langchain_core.messages import SystemMessage

from app.engine.execution_context import ExecutionContext
from app.engine.memory import MemoryManager
from app.engine.pipeline.base import PipelineStep
from app.engine.prompt_manager import PromptManager


class MemoryStep(PipelineStep):
    """
    Builds the conversation messages for the current execution.
    """

    def __init__(
        self,
        memory_manager: MemoryManager,
    ):
        self.memory_manager = memory_manager

    async def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:

        context.conversation_id = (
            self.memory_manager.get_or_create_conversation_id(
                context.conversation_id,
            )
        )

        history = await self.memory_manager.get_messages(
            context.conversation_id,
        )

        context.messages = [
            SystemMessage(
                content=PromptManager.get_default_prompt(),
            ),
            *history,
            context.input_message,
        ]

        return context
