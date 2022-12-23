import datetime as _date
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    body = Column(String(500), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    date_created = Column(DateTime, default=_date.datetime.utcnow)

    owner = relationship(
        "User", foreign_keys=[owner_id], 
         back_populates="blogs"
    )
