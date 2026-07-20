from pathlib import Path

from app.chunking.manager import ChunkManager
from app.chunking.strategies.recursive import (
    RecursiveChunkingStrategy,
)
from app.document.manager import DocumentManager

document = DocumentManager.parse(
    Path("tests/documents/sample.txt")
)

manager = ChunkManager(
    RecursiveChunkingStrategy(),
)

result = manager.chunk(
    document,
)

print("=" * 60)
print("Document ID :", result.document_id)
print("Strategy    :", result.strategy_name)
print("Chunks      :", result.total_chunks)
print("=" * 60)

for chunk in result.chunks:

    print("-" * 40)
    print(chunk.chunk_index)
    print(chunk.content[:100])