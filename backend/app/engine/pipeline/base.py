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
        pass