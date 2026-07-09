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