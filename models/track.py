from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key = True)
    filepath = Column(String, nullable = False)
    name = Column(String, nullable = False)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    track_number = Column(Integer, nullable=True)

    artist = relationship("Artist", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")


    @classmethod
    def create(cls, name, filepath, artist_id, album_id=None, track_number=None, session=None):
        
        if album_id and track_number is None:
            raise ValueError("Track number required for album tracks")
        
        track = cls(
            name=name,
            filepath=filepath,
            artist_id=artist_id,
            album_id=album_id,
            track_number=track_number
        )
        session.add(track)
        session.commit()
        return track
