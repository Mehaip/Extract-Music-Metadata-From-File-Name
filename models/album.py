from django.db import models
from .artist import Artist

class Album(models.Model):
    name = models.CharField(max_length = 200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)