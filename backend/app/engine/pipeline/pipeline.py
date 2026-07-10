from app.engine.execution_context import ExecutionContext
from app.engine.pipeline.base import PipelineStep


class ExecutionPipeline:
    """
    Executes pipeline steps sequentially.
    """

    def __init__(
        self,
        steps: list[PipelineStep],
    ):
        self.steps = steps

    async def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:

        for step in self.steps:
            context = await step.execute(context)

        return context

    async def stream(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:

        if not self.steps:
            return context

        # Execute every step except the last one normally.
        for step in self.steps[:-1]:
            context = await step.execute(context)

        # Let the last step produce the stream.
        context = await self.steps[-1].stream(context)

        return context