from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album    ")

    
    @classmethod
    def create(cls, name, artist_id, session):
        album = cls(
            name=name,
            artist_id=artist_id,
        )

        session.add(album)
        session.commit()
        return album