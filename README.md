# Spotify Playlist CSV Importer

A Python script that allows you to import songs from a CSV file into a Spotify playlist. The script can either create a new playlist or update an existing one.

## Features

- Import songs from a CSV file to Spotify
- Create new playlists or update existing ones
- Batch processing to handle large playlists
- Automatic track matching using Spotify's search API
- Handles authentication securely

## Prerequisites

- Python 3.x
- A Spotify account
- Spotify Developer credentials (Client ID and Client Secret)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/spotify-csv-importer.git
cd spotify-csv-importer
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required package:
```bash
pip install spotipy
```

4. Set up your Spotify credentials as environment variables:
```bash
export SPOTIPY_CLIENT_ID='your_client_id_here'
export SPOTIPY_CLIENT_SECRET='your_client_secret_here'
```

## Usage

1. Prepare your CSV file with two columns:
   - `Artist`: The name of the artist
   - `Track`: The name of the track

2. Run the script with the required arguments:
```bash
python import_spotify.py --playlist "Your Playlist Name" --csv "your_playlist.csv"
```

Or using the short form:
```bash
python import_spotify.py -p "Your Playlist Name" -c "your_playlist.csv"
```

3. Follow the authentication process:
   - Visit the provided URL
   - Log in to Spotify
   - Authorize the application
   - Copy the authorization code
   - Paste the code back into the terminal

The script will then:
- Check if a playlist with the given name exists
- Create a new playlist or update the existing one
- Import all tracks from your CSV file
- Show progress as it adds tracks in batches

## CSV File Format

Your CSV file should have the following format:
```csv
Artist,Track
Artist Name 1,Song Title 1
Artist Name 2,Song Title 2
...
```

## Security Notes

- Never commit your Spotify credentials to the repository
- Keep your `.env` file (if used) in your `.gitignore`
- The script uses environment variables for secure credential management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Contributing

Feel free to submit issues and enhancement requests!

## Running Tests

Install the development requirements and run `pytest`:
```bash
pip install -r requirements.txt
pytest
```
