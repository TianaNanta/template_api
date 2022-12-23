from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import blogs, users
from app.core.config import settings


root_api_rooter = APIRouter(prefix="/api")
root_api_rooter.include_router(blogs.router)
root_api_rooter.include_router(users.auth)
root_api_rooter.include_router(users.router)

def create_database():
    return Base.metadata.create_all(bind=engine)


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

create_database()

app = get_application()
