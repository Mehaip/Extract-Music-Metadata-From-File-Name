from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")