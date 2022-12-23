from pydantic import BaseModel
import datetime as _dt


class UserBase(BaseModel):
    name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str
    
    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    date_created: _dt.datetime
    is_active: bool

    class Config:
        orm_mode = True
