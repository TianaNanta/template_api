from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from ..database import get_db, engine

models.Base.metadata.create_all(engine)

router = APIRouter(prefix="/blogs")


# Create blog
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Blog)
def create_blog(blog: schemas.BlogBase, db: Session = Depends(get_db)):

    new_blog = models.Blog(title=blog.title, body=blog.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# List blogs
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Blog])
def list_blogs(db: Session = Depends(get_db)):

    blogs = db.query(models.Blog).all()

    return blogs


# Get blog by id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog)
def get_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")

    return blog


# Delete blog by id
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):

    blog_to_delete = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
    else:
        blog_to_delete.delete(synchronize_session=False)

        db.commit()

    return 'blog deleted successfully'


# Update blog
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.BlogBase,db: Session = Depends(get_db)):

    blog_to_update = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
    else:
        blog_to_update.update(request)
        db.commit()

    return 'updated successfully'