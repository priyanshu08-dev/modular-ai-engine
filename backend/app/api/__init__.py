from fastapi import APIRouter

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.document import router as document_router
from app.api.retrieval import router as retrieval_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(chat_router)
api_router.include_router(document_router)
api_router.include_router(retrieval_router)