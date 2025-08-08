from mutagen import File
from mutagen.easyid3 import EasyID3 
from mutagen.mp3 import MP3

class MetadataModifier:
    def __init__(self, audio_filepath: str, song_genius_id):
        self.audio_filepath = audio_filepath
        self.song_genius_id = song_genius_id

    
    def mp3Modifier(self):
        audio_file = EasyID3(self.audio_filepath)
        audio_file['title'] = "saluf"

        audio_file.save()

