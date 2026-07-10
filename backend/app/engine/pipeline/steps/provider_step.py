from collections.abc import AsyncIterator

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
        self.provider = ProviderFactory.get_provider()
        self.memory_manager = memory_manager

    async def _stream_response(
        self,
        context: ExecutionContext,
    ) -> AsyncIterator[str]:
        """
        Streams the provider response while accumulating the
        final response for conversation memory.
        """

        chunks: list[str] = []

        async for chunk in self.provider.stream(
            context.messages,
        ):
            chunks.append(chunk)
            yield chunk

        response = "".join(chunks)

        context.response = response

        await self.memory_manager.save_messages(
            context.conversation_id,
            [
                context.input_message,
                AIMessage(
                    content=response,
                ),
            ],
        )

    async def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:
        """
        Consume the stream and return the complete response.
        """

        async for _ in self._stream_response(
            context,
        ):
            pass

        return context

    async def stream(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:
        """
        Expose the streaming response.
        """

        context.stream = self._stream_response(
            context,
        )

        return context