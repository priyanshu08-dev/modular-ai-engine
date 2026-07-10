from abc import ABC, abstractmethod

from app.engine.execution_context import ExecutionContext


class PipelineStep(ABC):
    """
    Base class for every execution pipeline step.
    """

    @abstractmethod
    async def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:
        """
        Standard execution.
        """
        pass

    async def stream(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:
        """
        Default streaming behavior.

        Most pipeline steps behave identically for both
        synchronous and streaming execution, so streaming
        simply delegates to execute().
        """

        return await self.execute(context)