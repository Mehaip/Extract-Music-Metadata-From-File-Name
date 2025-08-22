from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)

    albums = relationship("Album", back_populates="artist")
    tracks = relationship("Track", back_populates="artist")

    @classmethod
    def create(cls, name, session):
        artist = cls(
            name=name
        )
        session.add(artist)
        session.commit()
        return artist
