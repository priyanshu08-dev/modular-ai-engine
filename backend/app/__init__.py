from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.config.settings import settings
from app.core.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.

    Everything that should happen when the application
    starts or stops belongs here.
    """

    print("🚀 Starting Modular AI Engine...")

    yield

    print("🛑 Shutting down Modular AI Engine...")


def create_app() -> FastAPI:
    """
    Application Factory
    """

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    register_exception_handlers(app)

    app.include_router(api_router)

    return app