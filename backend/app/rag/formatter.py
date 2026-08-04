from typing import Sequence

from app.rag.exceptions import ContextFormattingError
from app.rag.models import RAGContext, SourceAttribution
from app.retrieval.models import RetrievedChunk


class ContextFormatter:
    """
    Transforms retrieved document chunks into clean markdown-formatted
    context blocks for prompt injection and source attribution records.
    """

    @staticmethod
    def format_chunks(
        query: str,
        chunks: Sequence[RetrievedChunk],
        snippet_length: int = 150,
    ) -> RAGContext:
        """
        Formats retrieved chunks into a grounded context block.
        """
        try:
            if not chunks:
                return RAGContext(
                    query=query,
                    formatted_context="",
                    sources=[],
                    total_sources=0,
                    has_relevant_context=False,
                )

            formatted_blocks: list[str] = []
            sources: list[SourceAttribution] = []

            for idx, chunk in enumerate(chunks, start=1):
                block = (
                    f"--- Source [{idx}] (Document ID: {chunk.document_id}, "
                    f"Chunk ID: {chunk.chunk_id}, Relevance Score: {chunk.score:.4f}) ---\n"
                    f"{chunk.content.strip()}\n"
                )
                formatted_blocks.append(block)

                snippet = chunk.content.strip()
                if len(snippet) > snippet_length:
                    snippet = f"{snippet[:snippet_length]}..."

                sources.append(
                    SourceAttribution(
                        document_id=chunk.document_id,
                        chunk_id=chunk.chunk_id,
                        score=chunk.score,
                        content_snippet=snippet,
                        metadata=chunk.metadata,
                    )
                )

            context_text = "\n".join(formatted_blocks)

            return RAGContext(
                query=query,
                formatted_context=context_text,
                sources=sources,
                total_sources=len(sources),
                has_relevant_context=True,
            )

        except Exception as exc:
            raise ContextFormattingError(
                "Failed to format retrieved chunks into RAG context."
            ) from exc
