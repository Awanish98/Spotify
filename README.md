# Spotify_last_50
this python file fetche your past listening history and group them by making playlist of them 

## first you have to visit spotify developer mode on any browser to get api to access and manipulating in the data

# Spotify Playlist Automation

This script interacts with the Spotify API to automate the process of creating a playlist from recently played tracks. It uses the `spotipy` library for accessing the Spotify Web API.

## Requirements

- Python 3.x
- `spotipy` library

Install the `spotipy` library using pip if you haven't already:

```bash
pip install spotipy
```

## Setup

1. **Spotify Credentials:**
   - **Client ID:** Obtain this from the Spotify Developer Dashboard.
   - **Client Secret:** Obtain this from the Spotify Developer Dashboard.
   - **Redirect URI:** Ensure this matches the URI specified in your Spotify app settings.

2. **Configuration:**
   Update the `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` variables in the script with your Spotify application credentials.

## Script Overview

### Imports

```python
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
```

- `os` is used for file operations.
- `spotipy` is the library used to interact with the Spotify API.
- `SpotifyOAuth` handles authentication with Spotify.

### Spotify Credentials and Settings

```python
CLIENT_ID = '708d6e7a6ad74a81883ed6e1ddf02'
CLIENT_SECRET = '64f88fa2e5fb41e583fdbbf1c6d'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-read-recently-played playlist-modify-public playlist-modify-private'
CACHE_PATH = f".cache-{CLIENT_ID}"
```

- **CLIENT_ID**: Your Spotify application client ID.
- **CLIENT_SECRET**: Your Spotify application client secret.
- **REDIRECT_URI**: The redirect URI specified in your Spotify app settings.
- **SCOPE**: The scopes required for accessing the user’s recently played tracks and modifying playlists.
- **CACHE_PATH**: Path to the cache file used for storing authentication tokens.

### Cache File Management

```python
if os.path.exists(CACHE_PATH):
    os.remove(CACHE_PATH)
    print(f"Deleted cache file: {CACHE_PATH}")
```

- Deletes the cache file if it exists to ensure fresh authentication.

### Initialize Spotify Client

```python
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=CACHE_PATH
))
```

- Initializes the Spotify client with OAuth authentication.

### Functions

#### `get_recently_played_tracks(limit=50)`

```python
def get_recently_played_tracks(limit=50):
    """Get the recently played tracks"""
    try:
        results = sp.current_user_recently_played(limit=limit)
        tracks = [item['track']['id'] for item in results['items']]
        return tracks
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred: {e}")
        return []
```

- Retrieves a list of recently played tracks.
- Handles exceptions if any error occurs during the API call.

#### `create_playlist(name, description)`

```python
def create_playlist(name, description):
    """Create a new playlist"""
    try:
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user_id, name, description=description)
        return playlist['id']
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred: {e}")
        return None
```

- Creates a new playlist with the specified name and description.
- Handles exceptions if playlist creation fails.

#### `add_tracks_to_playlist(playlist_id, track_ids)`

```python
def add_tracks_to_playlist(playlist_id, track_ids):
    """Add tracks to the playlist"""
    try:
        sp.playlist_add_items(playlist_id, track_ids)
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred: {e}")
```

- Adds tracks to the specified playlist.
- Handles exceptions if adding tracks fails.

### Main Function

```python
def main():
    # Get the recently played tracks
    print("Fetching recently played tracks...")
    track_ids = get_recently_played_tracks(limit=50)

    if track_ids:
        # Create a new playlist
        playlist_name = "My Recently Played Tracks"
        playlist_description = "Playlist created from recently played tracks"
        print("Creating playlist...")
        playlist_id = create_playlist(playlist_name, playlist_description)

        if playlist_id:
            # Add tracks to the playlist
            print("Adding tracks to the playlist...")
            add_tracks_to_playlist(playlist_id, track_ids)
            print("Playlist created and tracks added successfully!")
        else:
            print("Failed to create playlist.")
    else:
        print("Failed to fetch recently played tracks.")

if __name__ == '__main__':
    main()
```

- **Fetches** recently played tracks.
- **Creates** a new playlist.
- **Adds** tracks to the newly created playlist.
- Prints status messages throughout the process.

## Running the Script

1. Save the script as `spotify_playlist.py`.
2. Run the script using Python:

```bash
python spotify_playlist.py
```

## Troubleshooting

- Ensure that your `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` are correct.
- Verify that the `CACHE_PATH` is accessible and writable.
- Check your Spotify Developer Dashboard for proper permissions and app settings.

---
