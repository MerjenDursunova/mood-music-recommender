import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "372de103b565467bbc58f2ee51e44c12")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "f851abc61c8440e9978b2af8a554dfaa")

def get_spotify_client():
    try:
        auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        
        sp = spotipy.Spotify(
            auth_manager=auth_manager,
            requests_timeout=20,
            retries=3
        )
        
        return sp
    except Exception as e:
        logger.error(f"Failed to authenticate with Spotify: {e}")
        raise


def search_songs_by_mood(mood, limit=10):
    try:
        sp = get_spotify_client()
        
        results = sp.search(q=mood, type="track", limit=limit)
        tracks = results["tracks"]["items"]
        
        if not tracks:
            logger.warning(f"No tracks found for mood: {mood}")
            return []
        
        
        track_ids = [item["id"] for item in tracks]
        
        
        try:
            features_list = sp.audio_features(track_ids)
        except Exception as e:
            logger.error(f"Failed to get audio features: {e}")
            return []
        
        songs = []
        
        for item, features in zip(tracks, features_list):
           
            if features is None or features.get("energy") is None:
                logger.debug(f"Skipping track {item.get('name', 'Unknown')} - no features available")
                continue
            
            try:
                song = {
                    "name": item["name"],
                    "artist": item["artists"][0]["name"] if item.get("artists") else "Unknown",
                    "url": item["external_urls"]["spotify"],
                    "energy": features["energy"],
                    "valence": features["valence"]
                }
                songs.append(song)
            except KeyError as e:
                logger.debug(f"Missing data for track: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(songs)} songs for mood '{mood}'")
        return songs  
    
    except Exception as e:
        logger.error(f"SPOTIFY ERROR: {type(e).__name__}: {e}")
        return []
def filter_by_mood_features(songs, mood):
    
    filtered = []
    
    for song in songs:
        if mood == "happy":
            if song["valence"] > 0.6 and song["energy"] > 0.5:
                filtered.append(song)
        
        elif mood == "sad":
            if song["valence"] < 0.4:
                filtered.append(song)
        
        elif mood == "energetic":
            if song["energy"] > 0.7:
                filtered.append(song)
        
        elif mood == "calm":
            if song["energy"] < 0.4:
                filtered.append(song)
        
        elif mood == "focused":
            if song["energy"] < 0.5 and song["valence"] < 0.5:
                filtered.append(song)
    
    return filtered