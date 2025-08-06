import os
import requests
import json
import csv
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

class GeniusAudioParser:
    def __init__(self, genius_token: str):
        """
        Initialize with your Genius API token
        Get one free at: https://genius.com/api-clients
        """
        self.genius_token = genius_token
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {genius_token}"}
        
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
            r'\s*(160kbit_Opus)'
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
        print(query)
        # Apply cleanup patterns to remove common YouTube cruft
        for pattern in self.cleanup_patterns:
            query = re.sub(pattern, '', query, flags=re.IGNORECASE)

        # Elements to remove
        
        for char in self.characters_to_remove:
            query = query.replace(char,"")
        
        # Remove extra whitespace
        query = ' '.join(query.split())
        print (f"FINAL QUERY: {query}")
        return query.strip()
    
    def is_translation_artist(self, artist_name: str) -> bool:
        """
        Checks if artist's name is genius english translation (or any other modifications). This official genius account naming 
        is ususally found first, before the original song from the original artists.
        This issue is mainly for foreign songs (in my case spanish)
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

    def search_genius(self, query: str) -> Optional[Dict]:
        """
        Search Genius API for a song
        Returns the best match or None if no good match found
        """
        search_url = f"{self.base_url}/search"
        params = {"q": query}
        
        try:
            response = requests.get(search_url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data["response"]["hits"]:
                # Get the first (best) results
                candidates = []
                for hit in data["response"]["hits"][:3]:
                    song_info = hit["result"]
                    print(json.dumps(song_info, indent=2))
                    artist_name = song_info["primary_artist"]["name"]
                    #basic_album = song_info.get("album", {}).get("name") if song_info.get("album") else None
                    #fix album
                    if self.is_translation_artist(artist_name):
                        #print(f"Skipping translation {song_info['title']} - {artist_name}")
                        continue
                    else:
                        candidate = {
                            "title": song_info["title"],
                            "artist": artist_name,
                            "album": song_info.get("album"),
                            "featured_artists": [artist["name"] for artist in song_info.get("featured_artists", [])],
                            "pageviews": song_info.get("stats", {}).get("pageviews", 0)
                        }

                        candidates.append(candidate)
                    #sort candidates by pageviews
            if candidates:
                sorted_candidates = sorted(candidates, key=lambda x: x["pageviews"], reverse=True)
                best_find = sorted_candidates[0]
                print(f"FOUND SONG: Title: {best_find['title']} ||| Artist: {best_find['artist']}")
                return best_find
                
            
            print(f"Not found {query}")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching for '{query}': {e}")
            return None

    def process_folder(self, folder_path: str, audio_extensions: List[str] = None, delay: float = 0.5) -> List[Dict]:
        """
        Process all audio files in a folder using Genius API
        
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
                      if f.is_file() and f.suffix.lower() in audio_extensions]
        
        print(f"Found {len(audio_files)} audio files to process...")
        
        for i, file_path in enumerate(audio_files, 1):
            print(f"Processing {i}/{len(audio_files)}: {file_path.name}")
            
            search_query = self.clean_search_query(file_path.name)
            print(search_query)
            results.append(search_query)
        return results

    def save_to_csv(self, results: List[Dict], output_path: str):
        """Save results to CSV file"""
        fieldnames = ['filepath', 'artist', 'title', 'album',  'featured_artists']
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore')
            writer.writeheader()
            for result in results:
                writer.writerow(result)

    def save_to_json(self, results: List[Dict], output_path: str):
        """Save results to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(results, jsonfile, indent=2, ensure_ascii=False)

 

def main():
    print("Genius API Audio File Parser")
    print("=" * 40)
    
    # Get Genius API token from environment variable
    genius_token = os.getenv('GENIUS_API_TOKEN')
    if not genius_token:
        print("Error: GENIUS_API_TOKEN not found in environment variables!")
        print("Please create a .env file with your token:")
        print("GENIUS_API_TOKEN=your_token_here")
        print("\nGet a token free at: https://genius.com/api-clients")
        return
    
    # Get folder path
    folder_path = os.getenv('FOLDER_PATH')
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return
    
    # Initialize parser
    parser = GeniusAudioParser(genius_token)
    
    # Process files
    print("\nStarting processing...")
    results = parser.process_folder(folder_path)
    
    if not results:
        print("No audio files found in the specified folder!")
        return
    findings = []
    for song_name in results:
        findings.append(parser.search_genius(song_name))
    
    
    # Save results
    csv_path = os.path.join("db/", 'genius_audio_database.csv')
    json_path = os.path.join("db/", 'genius_audio_database.json')
    
    parser.save_to_csv(findings, csv_path)
    parser.save_to_json(findings, json_path)


if __name__ == "__main__":
    main()