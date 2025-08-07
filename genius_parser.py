import os
import requests
import json
import csv
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from lyricsgenius import Genius


class GeniusAudioParser:
    def __init__(self, genius_token: str):
        """
        Initialize with your Genius API token
        Get one free at: https://genius.com/api-clients
        """
        self.genius_token = genius_token
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {genius_token}"}
        self.genius = Genius(genius_token)
        # Common YouTube suffixes to clean up search queries
        self.cleanup_patterns = [
            r'\s*\(official.*?\)',
            r'\s*\[official.*?\]',
            r'\s*\(.*?video.*?\)',
            r'\s*\[.*?video.*?\]',
            r'\s*\(.*?audio.*?\)',
            r'\s*\[.*?audio.*?\]',
            r'\s*\(.*?lyrics.*?\)',
            r'\s*\[.*?lyrics.*?\]',
            r'\s*\(.*?HD.*?\)',
            r'\s*\[.*?HD.*?\]',
            r'\s*\(.*?4K.*?\)',
            r'\s*\[.*?4K.*?\]',
            r'\s*-\s*YouTube$',
            r'\s*\|\s*YouTube$',
            r'\s*(128kbit_AAC)',
            r'\s*(152kbit_Opus)',
            r'\s*(160kbit_Opus)',
            r'^\d\d' #01 02 03 at the start of the string (oftentimes found in album downloaded media)
        ]

        self.characters_to_remove = [
            "-",
            "(",
            ")",
            "!",
            "[",
            "]"
        ]

    
    def clean_search_query(self, filename: str) -> str:
        """Clean up filename for better Genius search results"""
        import re
        
        # Remove file extension
        query = Path(filename).stem
        # Apply cleanup patterns to remove common YouTube cruft
        for pattern in self.cleanup_patterns:
            query = re.sub(pattern, '', query, flags=re.IGNORECASE)

        # Elements to remove
        
        for char in self.characters_to_remove:
            query = query.replace(char,"")
        
        # Remove extra whitespace
        query = ' '.join(query.split())
        print(query)
        return query.strip()
    
    def is_translation_artist(self, artist_name: str) -> bool:
        """
        Checks if artist's name is/contains "genius english translation" (or any other alternatives).
        Genius has official accounts that translate songs in other languages. These accounts are categorized as artists.
        Therefore, oftentimes it happens that the first artist found is "Genius english translation" or similar names. 
        (long story short, the translated version is found before the original one)
        So, we have to skip the songs assigned to these artists.
        """
        translation_indicators = [
            "genius english translations",
            "translations",
            "english translations",
            "español",
            "french translations",
            "deutsche übersetzungen",
            "traducciones al español",
            "traduzioni italiane",
            "русские переводы"
        ]

        artist_lower = artist_name.lower()
        return any(indicator in artist_lower for indicator in translation_indicators)

    def search_genius(self, song_data: Dict) -> Optional[Dict]:
        """
        Search Genius API for a song
        Returns the best match or None if no good match found
        """
        song_filepath = song_data["filepath"]
        song_query = song_data["search_query"]
        search_url = f"{self.base_url}/search"
        params = {"q": song_query}
        
        try:


            response = requests.get(search_url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data["response"]["hits"]:
                # Get the first (best) results
                candidates = []
                for hit in data["response"]["hits"][:3]:
                    song_info = hit["result"]
                    artist_name = song_info["primary_artist"]["name"]
                    #Check if the data is a translated version of the song (if it is, skip)
                    if self.is_translation_artist(artist_name):
                        #print(f"Skipping translation {song_info['title']} - {artist_name}")
                        continue
                    else: #Found the original song
                        song_complete_data = self.genius.song(song_info["id"])
                       ## print("="*40)
                       ## print(song_complete_data)
                       ## print("="*40)
                        album = (song_complete_data or {}).get('song', {}).get('album')
                        candidate = {
                            "title": song_info["title"],
                            "artist": artist_name,
                            "album": album.get('name') if album else None,
                            "album_genius_id": album.get('id') if album else None,
                            "featured_artists": [artist["name"] for artist in song_info.get("featured_artists", [])],
                            "filepath":song_filepath,
                            "pageviews": song_info.get("stats", {}).get("pageviews", 0) #pageviews for sorting by popularity (we can avoid remixes, covers, etc...)
                        }

                        candidates.append(candidate)
            #sort candidates by pageviews
            if candidates:
                sorted_candidates = sorted(candidates, key=lambda x: x["pageviews"], reverse=True) #sort by most popular (for now), maybe will need a revisit
                best_find = sorted_candidates[0]
                print(f"FOUND SONG: Title: {best_find['title']} ||| Artist: {best_find['artist']}")
                return best_find
                
            
            print(f"Not found {song_query}")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching for '{song_query}': {e}")
            return None

    def process_folder(self, folder_path: str, audio_extensions: List[str] = None, delay: float = 0.5) -> List[Dict]:
        """
        Process all audio files in a folder
        
        Args:
            folder_path: Path to folder containing audio files
            audio_extensions: List of audio file extensions to process
            delay: Delay between API calls to respect rate limits
        """
        if audio_extensions is None:
            audio_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.opus']
        
        results = []
        folder = Path(folder_path)
        
        audio_files = [f for f in folder.iterdir() 
                      if f.is_file() and f.suffix.lower() in audio_extensions] #we add only the audio files that have the specific audio_extensions that are in the folder
        
        print(f"Found {len(audio_files)} audio files to process...")
        
        for i, file_path in enumerate(audio_files, 1):
            print(f"Processing {i}/{len(audio_files)}: {file_path.name}")
            
            search_query = self.clean_search_query(file_path.name)
            complete_data = {
                "filepath": file_path.absolute(),
                "search_query":search_query
            }
            results.append(complete_data)
        return results

    def save_to_csv(self, results: List[Dict], output_path: str):
        """Save results to CSV file"""
        fieldnames = ['filepath', 'artist', 'title', 'album', 'album_genius_id',  'featured_artists']
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore')
            writer.writeheader()
            for result in results:
                writer.writerow(result)
