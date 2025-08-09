import os
from dotenv import load_dotenv
from audio_organizer import AudioOrganizer
from metadata_modifier import MetadataModifier
import sqlite3
from models import *
# Load environment variables from .env file
load_dotenv()


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
    organizer = AudioOrganizer(genius_token)
    
    # Process files
    results = organizer.process_folder(folder_path)
    if not results:
        print("No audio files found in the specified folder!")
        return
    findings = []
    for song_data in results:
        findings.append(organizer.search_genius(song_data))
    print(type(findings[0]))
    print(findings[0])

    #db

    tracks = [Track(**item) for item in findings]


    # Change file metadata & naming

    # modifier = MetadataModifier("music/in_rainbow/01 - Radiohead - 15 Step.MP3",123)
    # modifier.mp3Modifier()


    # Save results
    database_path = os.getenv("DATABASE_PATH", 'db/')
    os.makedirs(database_path, exist_ok=True)
    csv_path = os.path.join(database_path, 'songs.csv')
    
    organizer.save_to_csv(findings, csv_path)


if __name__ == "__main__":
    main()