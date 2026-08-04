from dataclasses import asdict

from langchain_core.messages import SystemMessage

from app.config.settings import settings
from app.engine.execution_context import ExecutionContext
from app.engine.pipeline.base import PipelineStep
from app.rag.manager import RAGManager
from app.rag.prompt import RAGPromptBuilder


class RAGStep(PipelineStep):
    """
    Pipeline step that performs semantic knowledge retrieval, formats
    context blocks, and updates the execution messages with grounded prompts.
    """

    def __init__(
        self,
        rag_manager: RAGManager | None = None,
    ) -> None:
        self.rag_manager = rag_manager or RAGManager()

    async def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:
        """
        Executes RAG context retrieval if RAG is enabled for this request.
        """
        enable_rag = context.metadata.get("enable_rag", settings.RAG_ENABLED)

        if not enable_rag:
            context.metadata["rag_enabled"] = False
            return context

        query = context.input_message.content

        top_k = context.metadata.get("top_k") or settings.RAG_TOP_K
        score_threshold = (
            context.metadata.get("score_threshold")
            if context.metadata.get("score_threshold") is not None
            else settings.RAG_SCORE_THRESHOLD
        )
        document_id = context.metadata.get("document_id")

        rag_context = await self.rag_manager.retrieve_context(
            query=query,
            top_k=top_k,
            score_threshold=score_threshold,
            document_id=document_id,
        )

        context.metadata["rag_enabled"] = True
        context.metadata["rag_context"] = rag_context
        context.metadata["sources"] = [
            asdict(source) for source in rag_context.sources
        ]

        rag_system_prompt = RAGPromptBuilder.build_system_prompt(rag_context)

        if context.messages and isinstance(context.messages[0], SystemMessage):
            context.messages[0] = SystemMessage(content=rag_system_prompt)
        else:
            context.messages.insert(0, SystemMessage(content=rag_system_prompt))

        return context
