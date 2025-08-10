from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Artist(Base):
    __tablename__ = "Artists"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    artist = Column(Integer, ForeignKey("artists.id"))
