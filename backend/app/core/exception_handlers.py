from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.document.exceptions import (
    InvalidDocumentError,
    UnsupportedDocumentError,
    DocumentParsingError,
)

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UnsupportedDocumentError)
    async def unsupported_document_handler(
        request: Request,
        exc: UnsupportedDocumentError,
    ):
        return JSONResponse(
            status_code=415,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(InvalidDocumentError)
    async def invalid_document_handler(
        request: Request,
        exc: InvalidDocumentError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(DocumentParsingError)
    async def parsing_handler(
        request: Request,
        exc: DocumentParsingError,
    ):
        return JSONResponse(
            status_code=422,
            content={
                "detail": str(exc),
            },
        )
