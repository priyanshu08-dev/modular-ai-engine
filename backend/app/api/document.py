from fastapi import APIRouter, File, UploadFile, status

from app.document.mapper import DocumentMapper
from app.schemas.document import DocumentIngestResponse, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService()


@router.post(
    "/parse",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
)
async def parse_document(
    file: UploadFile = File(...),
):
    """Parses document file and returns extracted text and metadata."""
    document = await document_service.parse_document(file)
    return DocumentMapper.to_response(document)


@router.post(
    "/ingest",
    response_model=DocumentIngestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_document(
    file: UploadFile = File(...),
):
    """
    Executes complete ingestion pipeline: Upload -> Parse -> Chunk -> Embed -> Store in Vector Store.
    """
    result = await document_service.ingest_document(file)
    return DocumentIngestResponse(
        document_id=str(result["document_id"]),
        filename=str(result["filename"]),
        document_type=str(result["document_type"]),
        total_chunks=int(result["total_chunks"]),  # type: ignore[arg-type]
        status=str(result["status"]),
    )
