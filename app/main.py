from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router import root_api_rooter

from app.core.config import settings


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, docs_url="/", redoc_url="/api")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(root_api_rooter)

    return _app


app = get_application()
