from fastapi import APIRouter
from .users import crud as userCrud
from .blogs import crud as blogCrud

root_api_rooter = APIRouter(prefix="/api")

root_api_rooter.include_router(userCrud.router)
root_api_rooter.include_router(blogCrud.router)