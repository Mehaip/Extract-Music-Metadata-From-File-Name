from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.oggopus import OggOpus
from mutagen.mp4 import MP4
from pathlib import Path

class MetadataModifier:
    
    def mp3Modifier(self, song):
        path = str(song["filepath"])
        mp3file = MP3(path, ID3=EasyID3)
        mp3file['album'] = song['album']
        mp3file['albumartist'] = song['artist']
        mp3file['title'] = song['title']
        mp3file.save()
        print(" MP3 metadata updated")
    
    def opusModifier(self, song):
        path = str(song["filepath"])
        opusfile = OggOpus(path)
        opusfile['album'] = song['album']
        opusfile['albumartist'] = song['artist']
        opusfile['title'] = song['title']
        opusfile.save()
        print(" OPUS metadata updated")

    def m4aModifier(self, song):
        path = str(song["filepath"])
        print(path)
        m4afile = MP4(path)
        
        # M4A uses different tag names with special characters
        m4afile['\xa9alb'] = song['album']      # Album
        m4afile['aART'] = song['artist']        # Album Artist
        m4afile['\xa9nam'] = song['title']      # Title
        
        m4afile.save()
        print("✅ M4A metadata updated")