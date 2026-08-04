import sys
from pathlib import Path

# Add the 'backend/' directory to Python's import search path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio

from app.engine.core import AIEngine
from app.services.document_service import DocumentService
from fastapi import UploadFile


async def main() -> None:
    print("=" * 70)
    print("Milestone 15 — RAG Subsystem Integration Playground")
    print("=" * 70)

    sample_file = Path("tests/documents/sample.txt")
    if not sample_file.exists():
        print(f"Error: Sample document not found at {sample_file}")
        return

    doc_service = DocumentService()

    print("\n1. Ingesting sample document into ChromaDB...")
    with sample_file.open("rb") as f:
        upload_file = UploadFile(
            filename=sample_file.name,
            file=f,  # type: ignore[arg-type]
        )
        ingest_res = await doc_service.ingest_document(upload_file)

    print(f"   ✓ Ingested Document ID : {ingest_res['document_id']}")
    print(f"   ✓ Total Chunks         : {ingest_res['total_chunks']}")

    engine = AIEngine()
    query = "How many animal species have been described?"

    print(f"\n2. Executing RAG-grounded query:\n   '{query}'\n")

    conv_id, response, context = await engine.run(
        message=query,
        enable_rag=True,
        top_k=3,
        score_threshold=0.2,
    )

    print("=" * 70)
    print("RAG GROUNDED RESPONSE")
    print("=" * 70)
    print(response)

    print("\n" + "=" * 70)
    print("SOURCE ATTRIBUTIONS")
    print("=" * 70)
    sources = context.metadata.get("sources", [])
    print(f"Total Sources Retrieved: {len(sources)}")

    for idx, source in enumerate(sources, 1):
        print(f"\n[{idx}] Document ID : {source['document_id']}")
        print(f"    Chunk ID    : {source['chunk_id']}")
        print(f"    Score       : {source['score']}")
        print(f"    Snippet     : {source['content_snippet']}")

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())