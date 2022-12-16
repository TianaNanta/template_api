from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_blogs():
    return "blogs app created!"
