from pathlib import Path

from app.document.exceptions import DocumentError
from app.document.manager import DocumentManager

try:

    document = DocumentManager.parse(
        Path("tests/documents/sample.pdf")
    )

    print("=" * 60)
    print("Document Type :", document.document_type)
    print("Filename      :", document.metadata.filename)
    print("MIME Type     :", document.metadata.mime_type)
    print("File Size     :", document.metadata.size)
    print("Pages         :", document.metadata.page_count)
    print("Characters    :", document.metadata.character_count)
    print("Words         :", document.metadata.word_count)
    print("-" * 60)
    print(document.content[:500])
    print("=" * 60)

except DocumentError as e:
    print(e)