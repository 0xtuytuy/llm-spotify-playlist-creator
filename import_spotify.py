import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Import songs from a CSV file into a Spotify playlist.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Create or update a playlist with songs from a CSV file
  python import_spotify.py --playlist "My Awesome Playlist" --csv "songs.csv"
  
  # Using short form arguments
  python import_spotify.py -p "My Awesome Playlist" -c "songs.csv"
  
  # Show this help message
  python import_spotify.py --help
        '''
    )
    parser.add_argument('--playlist', '-p', 
                      required=True,
                      metavar='NAME',
                      help='Name of the playlist to create or update (will be created if it doesn\'t exist)')
    parser.add_argument('--csv', '-c',
                      required=True,
                      metavar='FILE',
                      help='Path to the CSV file containing the songs (must have Artist and Track columns)')
    return parser.parse_args()

def main():
    # Parse arguments first
    args = parse_arguments()
    
    # Spotify API credentials
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback/'

    if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
        print(
            'Error: SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables must be set.'
        )
        sys.exit(1)

    # Define the scope for the playlist modification
    scope = 'playlist-modify-public'

    # Initialize the SpotifyOAuth object but don't open the browser
    auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                client_secret=SPOTIPY_CLIENT_SECRET,
                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                scope=scope,
                                open_browser=False)

    # Manually get the auth URL and prompt the user to visit it
    auth_url = auth_manager.get_authorize_url()
    print(f"Please go to the following URL to authorize the application: {auth_url}")

    # After visiting the URL, you'll get a code parameter in the URL; enter it here
    auth_response_code = input("Enter the authorization code from the URL: ")

    # Now, use the code to get the access token
    token_info = auth_manager.get_access_token(auth_response_code)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_name = args.playlist
    csv_file = args.csv

    # Step 1: Check if playlist exists or create new one
    user_id = sp.current_user()['id']

    # Search for existing playlists
    playlists = sp.current_user_playlists()
    existing_playlist = None
    while playlists:
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                existing_playlist = playlist
                break
        if existing_playlist or not playlists['next']:
            break
        playlists = sp.next(playlists)

    if existing_playlist:
        print(f"Found existing playlist: {playlist_name}")
        playlist_id = existing_playlist['id']
        # Clear existing tracks
        sp.playlist_replace_items(playlist_id, [])
        print("Cleared existing tracks from playlist")
    else:
        print(f"Creating new playlist: {playlist_name}")
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        playlist_id = playlist['id']

    # Step 2: Read songs from the CSV file
    def get_song_uri(artist, track):
        query = f"artist:{artist} track:{track}"
        result = sp.search(q=query, type='track', limit=1)
        tracks = result.get('tracks', {}).get('items', [])
        if tracks:
            return tracks[0]['uri']
        return None

    # Step 3: Add songs to the playlist
    def add_songs_to_playlist(csv_file, playlist_id):
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            track_uris = []
            for row in reader:
                artist = row['Artist']
                track = row['Track']
                uri = get_song_uri(artist, track)
                if uri:
                    track_uris.append(uri)
                else:
                    print(f"Track not found: {artist} - {track}")
            
            # Add tracks to the playlist in batches of 100
            if track_uris:
                batch_size = 100
                for i in range(0, len(track_uris), batch_size):
                    batch = track_uris[i:i + batch_size]
                    try:
                        sp.playlist_add_items(playlist_id, batch)
                        print(f"Added batch of {len(batch)} tracks to the playlist!")
                    except Exception as e:
                        print(f"Error adding batch {i//batch_size + 1}: {str(e)}")
                print("Finished adding tracks to the playlist!")

    # Run the script
    add_songs_to_playlist(csv_file, playlist_id)

if __name__ == '__main__':
    # Check if --help or -h is in the arguments
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        parse_arguments()  # This will show help and exit
    else:
        main()