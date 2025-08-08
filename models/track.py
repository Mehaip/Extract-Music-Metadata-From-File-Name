from django.db import models
from pathlib import Path

class Track(models.Model):
    filepath = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500)
    #album = models.CharField(max_length=500)
    
    @property
    def file_path(self):
        return Path(self.filepath)