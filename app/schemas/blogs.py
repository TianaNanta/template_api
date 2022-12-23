from pydantic import BaseModel
from datetime import datetime

from app.schemas import users as schemas


class BlogBase(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True

class BlogCreate(BlogBase):
    pass


class Blog(BlogBase):
    id: int
    owner_id: int
    date_created: datetime
    owner: schemas.UserBase

    class Config:
        orm_mode = True
