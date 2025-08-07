import os
from dotenv import load_dotenv
from genius_parser import GeniusAudioParser

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
    parser = GeniusAudioParser(genius_token)
    
    # Process files
    results = parser.process_folder(folder_path)
    if not results:
        print("No audio files found in the specified folder!")
        return
    findings = []
    for song_data in results:
        findings.append(parser.search_genius(song_data))
    
    
    # Save results
    csv_path = os.path.join("db/", 'genius_audio_database.csv')
    json_path = os.path.join("db/", 'genius_audio_database.json')
    
    parser.save_to_csv(findings, csv_path)
    parser.save_to_json(findings, json_path)


if __name__ == "__main__":
    main()