from django.db import models
from pathlib import Path
from .album import Album
from .artist import Artist

class Track(models.Model):
    filepath = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    
    @property
    def file_path(self):
        return Path(self.filepath)