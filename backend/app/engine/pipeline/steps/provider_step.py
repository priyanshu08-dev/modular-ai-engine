from langchain_core.messages import AIMessage

from app.engine.execution_context import ExecutionContext
from app.engine.memory import MemoryManager
from app.engine.pipeline.base import PipelineStep
from app.providers import ProviderFactory


class ProviderStep(PipelineStep):
    """
    Executes the configured LLM provider.
    """

    def __init__(
        self,
        memory_manager: MemoryManager,
    ):
        provider = ProviderFactory.get_provider()

        self.llm = provider.get_chat_model()
        self.memory_manager = memory_manager

    async def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:

        response = await self.llm.ainvoke(
            context.messages,
        )

        context.response = response.content

        await self.memory_manager.save_messages(
            context.conversation_id,
            [
                context.input_message,
                AIMessage(
                    content=response.content,
                ),
            ],
        )

        return context