# Import modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import pandas as pd
from pathlib import Path
from youtube_search import YoutubeSearch

# Spotify API credentials
client_id = ''
client_secret = ''

try:
    # Authorization
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    )

    # Get playlist tracks
    playlist_id = ''
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Get total number of tracks in the playlist
    total_tracks = sp.playlist(playlist_id)['tracks']['total']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Extract track info
    track_info = []

    for index, track in enumerate(tracks):
      
      # Search YouTube
      query = f"{track['track']['artists'][0]['name']} - {track['track']['name']}"
      yt_results = YoutubeSearch(query, max_results=1).to_dict()  
        
      youtube_link = ""
      if yt_results:
        youtube_link = f"https://youtube.com/watch?v={yt_results[0]['id']}"

      track_info.append({
        'Artist': track['track']['artists'][0]['name'], 
        'Track': track['track']['name'],
        'Album': track['track']['album']['name'],
        'Album_type': track['track']['album']['album_type'],
        'Title': track['track']['name'],
        'Url_youtube': youtube_link,
        'Released': track['track']['album']['release_date'].split('-')[0]
      })
      
      # Print progress
      progress = (index + 1) / total_tracks * 100
      print(f'Progress: {progress:.2f}%')

    # Create DataFrame 
    df = pd.DataFrame(track_info)

    # Export to Desktop
    desktop = Path.home() / 'Desktop' / 'Scripts' / 'MediaBrake_TikTok'
    output_file = desktop / 'spotify-single-playlist.xlsx'
    df.to_excel(output_file, index=False)

    print('Playlist exported to Desktop')
except Exception as e:
    print(f"An error occurred: {e}")