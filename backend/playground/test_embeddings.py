from __future__ import annotations

import asyncio

from app.chunking.models import (
    Chunk,
    ChunkMetadata,
    ChunkingResult,
)
from app.document.models import DocumentType
from app.embeddings.manager import EmbeddingManager


async def main() -> None:
    """
    Playground for manually testing embedding generation.
    """

    chunking_result = ChunkingResult(
        document_id="sample-document",
        strategy_name="recursive",
        chunks=[
            Chunk(
                chunk_id="chunk-1",
                document_id="sample-document",
                document_type=DocumentType.TXT,
                chunk_index=0,
                content="Artificial Intelligence is transforming software engineering.",
                metadata=ChunkMetadata(),
                start_char=0,
                end_char=61,
            ),
            Chunk(
                chunk_id="chunk-2",
                document_id="sample-document",
                document_type=DocumentType.TXT,
                chunk_index=1,
                content="Embeddings convert natural language into dense numerical vectors.",
                metadata=ChunkMetadata(),
                start_char=62,
                end_char=129,
            ),
        ],
    )

    manager = EmbeddingManager()

    result = await manager.generate_embeddings(
        chunking_result
    )

    print("=" * 60)
    print("Embedding Generation Result")
    print("=" * 60)

    print(f"Document ID : {result.document_id}")
    print(f"Embeddings  : {len(result.embeddings)}")

    for embedding in result.embeddings:

        print("-" * 60)
        print(f"Embedding ID : {embedding.embedding_id}")
        print(f"Chunk ID     : {embedding.chunk_id}")
        print(f"Dimensions   : {embedding.metadata.dimensions}")
        print(f"Provider     : {embedding.metadata.provider}")
        print(f"Model        : {embedding.metadata.model}")
        print(f"Vector Size  : {len(embedding.vector)}")

        print(
            f"Vector Preview : {embedding.vector[:5]}"
        )


if __name__ == "__main__":
    asyncio.run(main())