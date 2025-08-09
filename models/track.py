from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base


class Track(Base):
    __tablename__ = "Tracks"

    id = Column(Integer, primary_key = True)
    filepath = Column(String, nullable = False)
    title = Column(String, nullable = False)
    artist = Column(Integer, ForeignKey("artists.id"))
    album = Column(Integer, ForeignKey("albums.id"))