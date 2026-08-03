import asyncio
from pathlib import Path

from app.chunking.manager import ChunkManager
from app.chunking.strategies.recursive import RecursiveChunkingStrategy
from app.document.manager import DocumentManager
from app.embeddings.manager import EmbeddingManager
from app.retrieval.manager import RetrievalManager
from app.vectorstore.manager import VectorStoreManager


async def main() -> None:
    print("=" * 60)
    print("Milestone 14 - Retrieval Pipeline Validation Playground")
    print("=" * 60)

    sample_file = Path("tests/documents/sample.txt")
    if not sample_file.exists():
        print(f"Error: Sample file missing at {sample_file}")
        return

    print("1. Parsing document...")
    doc = DocumentManager.parse(sample_file)

    print("2. Chunking document...")
    chunk_mgr = ChunkManager(RecursiveChunkingStrategy())
    chunking_result = chunk_mgr.chunk(doc)
    print(f"Generated {chunking_result.total_chunks} chunks.")

    print("3. Generating embeddings...")
    embedding_mgr = EmbeddingManager()
    embedding_result = await embedding_mgr.generate_embeddings(chunking_result)

    print("4. Persisting vectors to ChromaDB...")
    vector_mgr = VectorStoreManager()
    await vector_mgr.store_embeddings(chunking_result, embedding_result)

    query = "How many animal species have been described?"
    print(f"\n5. Executing Semantic Search for Query:\n   '{query}'")

    retrieval_mgr = RetrievalManager()
    result = await retrieval_mgr.search(
        query=query,
        top_k=3,
        score_threshold=0.2,
    )

    print("\n" + "=" * 60)
    print("Retrieval Search Results")
    print("=" * 60)
    print(f"Strategy      : {result.strategy_name}")
    print(f"Total Matches : {result.total_results}")

    for idx, chunk in enumerate(result.chunks, 1):
        print("-" * 60)
        print(f"Match #{idx}")
        print(f"Chunk ID  : {chunk.chunk_id}")
        print(f"Doc ID    : {chunk.document_id}")
        print(f"Score     : {chunk.score}")
        print(f"Content   : {chunk.content[:120]}...")

    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
