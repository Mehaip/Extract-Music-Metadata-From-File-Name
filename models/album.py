from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Album(Base):
    __tablename__ = "Albums"
    id = Column(id, primary_key = True)