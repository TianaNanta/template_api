from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.schemas import blogs as schemas
from app import dependencies as crud
from app.database import get_db

# models.Base.metadata.create_all(engine)

router = APIRouter(prefix="/blogs", tags=['Blogs'])


# Create blog
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Blog)
def create_blog(blog: schemas.BlogBase, db: Session = Depends(get_db)):
    return crud.create_blog(blog, db)


# List blogs
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Blog])
def list_blogs(db: Session = Depends(get_db)):
    return crud.get_all_blogs(db)


# Get blog by id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog)
def get_blog(id, db: Session = Depends(get_db)):
    return crud.get_blog(id, db)


# Delete blog by id
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    return crud.delete_blog(id, db)


# Update blog
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Blog)
def update_blog(id, blog: schemas.BlogBase,db: Session = Depends(get_db)):
    return crud.update_blog(id, blog, db)
