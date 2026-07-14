from fastapi import APIRouter, File, UploadFile
from app.document.mapper import DocumentMapper

from app.schemas.document import (
    DocumentMetadataResponse,
    DocumentResponse,
)
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService()


@router.post(
    "/parse",
    response_model=DocumentResponse,
)
async def parse_document(
    file: UploadFile = File(...),
):

    document = await document_service.parse_document(
        file,
    )

    return DocumentMapper.to_response(
    document,
)
