import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials and settings
CLIENT_ID = '708d6e7a6ad74a81883ed6e1ddf02'
CLIENT_SECRET = '64f88fa2e5fb41e583fdbbf1c6d'
REDIRECT_URI = 'http://localhost:8888/callback'  # Update this to your new redirect URI
SCOPE = 'user-read-recently-played playlist-modify-public playlist-modify-private'

# Define the cache path
CACHE_PATH = f".cache-{CLIENT_ID}"

# Delete the cache file if it exists
if os.path.exists(CACHE_PATH):
    os.remove(CACHE_PATH)
    print(f"Deleted cache file: {CACHE_PATH}")

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=CACHE_PATH
))


def get_recently_played_tracks(limit=50):
    """Get the recently played tracks"""
    try:
        results = sp.current_user_recently_played(limit=limit)
        tracks = [item['track']['id'] for item in results['items']]
        return tracks
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred: {e}")
        return []


def create_playlist(name, description):
    """Create a new playlist"""
    try:
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user_id, name, description=description)
        return playlist['id']
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred: {e}")
        return None


def add_tracks_to_playlist(playlist_id, track_ids):
    """Add tracks to the playlist"""
    try:
        sp.playlist_add_items(playlist_id, track_ids)
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred: {e}")


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
