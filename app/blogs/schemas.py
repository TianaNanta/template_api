from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class ItemCreate(BlogBase):
    pass


class Item(BlogBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True