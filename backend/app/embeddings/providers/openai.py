from __future__ import annotations

import asyncio
from uuid import uuid4

from langchain_openai import OpenAIEmbeddings

from app.chunking.models import ChunkingResult
from app.config.settings import settings
from app.embeddings.exceptions import EmbeddingProviderError
from app.embeddings.models import (
    Embedding,
    EmbeddingMetadata,
    EmbeddingResult,
)
from app.embeddings.providers.base import BaseEmbeddingProvider


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """
    OpenAI implementation of the embedding provider.
    """

    def __init__(self) -> None:
        self._embeddings = OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )

    async def generate_embeddings(
        self,
        chunking_result: ChunkingResult,
    ) -> EmbeddingResult:
        """
        Generate embeddings for every chunk in the supplied ChunkingResult.
        """

        if not chunking_result.chunks:
            return EmbeddingResult(
                document_id=chunking_result.document_id,
                embeddings=[],
            )

        texts = [
            chunk.content
            for chunk in chunking_result.chunks
        ]

        try:
            vectors = await asyncio.to_thread(
                self._embeddings.embed_documents,
                texts,
            )

        except Exception as exc:
            raise EmbeddingProviderError(
                "Failed to generate OpenAI embeddings."
            ) from exc

        dimensions = len(vectors[0])

        metadata = EmbeddingMetadata(
            provider="openai",
            model=settings.OPENAI_EMBEDDING_MODEL,
            dimensions=dimensions,
        )

        embeddings = [
            Embedding(
                embedding_id=str(uuid4()),
                chunk_id=chunk.chunk_id,
                vector=vector,
                metadata=metadata,
            )
            for chunk, vector in zip(
                chunking_result.chunks,
                vectors,
                strict=True,
            )
        ]

        return EmbeddingResult(
            document_id=chunking_result.document_id,
            embeddings=embeddings,
        )

    async def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate embedding for a query string.
        """
        try:
            return await asyncio.to_thread(
                self._embeddings.embed_query,
                query,
            )
        except Exception as exc:
            raise EmbeddingProviderError(
                "Failed to generate OpenAI query embedding."
            ) from exc