import datetime as _date

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

from app.database import Base


pwd_txt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(300))
    date_created = Column(DateTime, default=_date.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    blogs = relationship(
        "Blog", foreign_keys="[Blog.owner_id]", back_populates="owner"
    )

    def verify_password(self, password: str):
        return pwd_txt.verify(password, self.hashed_password)
