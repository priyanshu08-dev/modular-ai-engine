from __future__ import annotations

from app.chunking.models import ChunkingResult
from app.embeddings.models import EmbeddingResult
from app.vectorstore.exceptions import (
    VectorStorageError,
)
from app.vectorstore.models import (
    VectorBatch,
    VectorRecord,
)


class VectorStoreMapper:
    """
    Maps upstream domain models into Vector Storage
    domain models.

    This keeps the Vector Store subsystem independent
    from the Chunking and Embedding implementations.
    """

    @staticmethod
    def to_vector_batch(
        chunking_result: ChunkingResult,
        embedding_result: EmbeddingResult,
    ) -> VectorBatch:
        """
        Converts ChunkingResult and EmbeddingResult into
        a VectorBatch ready for persistence.
        """

        chunk_lookup = {
            chunk.chunk_id: chunk
            for chunk in chunking_result.chunks
        }

        vectors: list[VectorRecord] = []

        for embedding in embedding_result.embeddings:

            chunk = chunk_lookup.get(
                embedding.chunk_id,
            )

            if chunk is None:
                raise VectorStorageError(
                    f"Chunk '{embedding.chunk_id}' "
                    "not found while mapping embeddings."
                )

            vectors.append(
                VectorRecord(
                    embedding_id=embedding.embedding_id,
                    chunk_id=embedding.chunk_id,
                    document_id=embedding_result.document_id,
                    content=chunk.content,
                    vector=list(embedding.vector),
                    metadata={
                        "document_id": embedding_result.document_id,
                        "chunk_id": embedding.chunk_id,
                        "provider": embedding.metadata.provider,
                        "model": embedding.metadata.model,
                        "dimensions": embedding.metadata.dimensions,
                        "filename": chunk.metadata.source or "unknown",
                    },
                )
            )

        return VectorBatch(
            document_id=embedding_result.document_id,
            vectors=vectors,
        )