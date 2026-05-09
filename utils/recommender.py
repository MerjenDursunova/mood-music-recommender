import pandas as pd
from sklearn.cluster import KMeans

def cluster_songs():
    df = load_data()
    
  
    X = df[["energy", "valence"]]
    
    
    kmeans = KMeans(n_clusters=5, random_state=42)
    
    df["cluster"] = kmeans.fit_predict(X)
    
    return df, kmeans

def recommend_from_cluster(mood, n=5):
    df, kmeans = cluster_songs()
    
    
    mood_targets = {
        "happy": [0.8, 0.8],
        "sad": [0.3, 0.2],
        "energetic": [0.9, 0.6],
        "calm": [0.2, 0.5],
        "focused": [0.4, 0.4]
    }
    
    target = mood_targets.get(mood, [0.5, 0.5])
    
    
    centers = kmeans.cluster_centers_
    

    import numpy as np
    distances = [np.linalg.norm(center - target) for center in centers]
    best_cluster = distances.index(min(distances))
    
  
    cluster_df = df[df["cluster"] == best_cluster]
    
    return cluster_df.sample(min(n, len(cluster_df)))

def load_data():
    df = pd.read_csv("data/songs.csv")
    return df

def recommend_songs(mood, n=5):
    df = load_data()
    
    
    results = df[df["mood"] == mood]
    
    
    if results.empty:
        return results
    
    
    results = results.sample(frac=1)
    
    
    return results.head(n)

from sklearn.metrics.pairwise import cosine_similarity

def get_similar_songs(mood, n=5):
    df = load_data()
    
    
    df_mood = df[df["mood"] == mood]
    
    if df_mood.empty:
        return df_mood
    
 
    features = df_mood[["energy", "valence"]]
    
    similarity = cosine_similarity(features)
    
  
    base_index = 0
    
    similar_indices = similarity[base_index].argsort()[::-1][1:n+1]
    
    return df_mood.iloc[similar_indices]