import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback/'

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

# Step 1: Create a new playlist
user_id = sp.current_user()['id']
playlist_name = "Enchanted Garden Party"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
playlist_id = playlist['id']

# Step 2: Read songs from the CSV file
csv_file = 'enchanted_garden_party_simplified_playlist.csv'  # Your CSV file path

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
        
        # Step 4: Add tracks to the playlist
        if track_uris:
            sp.playlist_add_items(playlist_id, track_uris)
            print("Tracks successfully added to the playlist!")

# Run the script
add_songs_to_playlist(csv_file, playlist_id)