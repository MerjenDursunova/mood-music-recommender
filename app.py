import streamlit as st
from utils.recommender import get_similar_songs
from utils.weather import get_weather, weather_to_mood
from utils.spotify_api import filter_by_mood_features, search_songs_by_mood
from utils.recommender import recommend_from_cluster
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


st.title(" Mood-Based Music Recommender")
st.caption("AI-powered music suggestions using mood, weather, and machine learning")



def get_youtube_embed(link):
    if "watch?v=" in link:
        video_id = link.split("watch?v=")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return link



city_input = st.text_input("Type a city")

city_dropdown = st.selectbox(
    "Or select a city:",
    ["Seoul", "Tokyo", "London", "New York", "Paris", "Dubai"]
)

city = city_input if city_input else city_dropdown


if city.strip() == "":
    city = "Seoul"


num_songs = st.slider("Number of recommendations:", 1, 10, 5)


weather_data = get_weather(city)

def get_background_image(weather):
    weather = weather.lower()
    
    if "clear" in weather:
        return "assets/sunny.jpeg"
    elif "rain" in weather:
        return "assets/rain.jpeg"
    elif "cloud" in weather:
        return "assets/cloudy.jpeg"
    elif "snow" in weather:
        return "assets/snow.jpeg"
    elif "clear" in weather:
        return "assets/sunny.jpeg"
    else:
        return "assets/default.jpeg"
    
if weather_data:
    bg_path = get_background_image(weather_data["weather"])
else:
    bg_path = "assets/default.jpg"

bg_base64 = get_base64_image(bg_path)

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    background-color: rgba(255, 255, 255, 0.7);
    padding: 2rem;
    border-radius: 15px;
}}
</style>
""", unsafe_allow_html=True)

if weather_data:
    weather = weather_data["weather"]
    temp = weather_data["temp"]
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    ">
        <h2> Weather in {city}</h2>
        <h1>{weather_data['temp']}°C</h1>
        <h3>{weather_data['weather']}</h3>
        <p> Feels like: {weather_data['feels_like']}°C</p>
        <p> Humidity: {weather_data['humidity']}%</p>
        <p> Wind: {weather_data['wind']} m/s</p>
    </div>
    """, unsafe_allow_html=True)

    suggested_mood = weather_to_mood(weather_data["weather"])
    st.markdown(f"###  Suggested Mood: **{suggested_mood}**")
else:
    st.error("⚠️ Could not fetch weather data. Try another city.")
    suggested_mood = "happy"


mood_list = ["happy", "sad", "energetic", "calm", "focused"]

mood = st.selectbox(
    "Choose your mood:",
    mood_list,
    index=mood_list.index(suggested_mood)
)

if st.button("Get Recommendations"):
    results = recommend_from_cluster(mood, num_songs)
    
    if results.empty:
        st.write("No songs found for this mood.")
    else:
        st.write("###  Your Dataset Recommendations:")
        
        for _, row in results.iterrows():
            st.markdown(f"""
            <div style="
                background-color:##FFD1DC;
                padding:20px;
                border-radius:15px;
                margin-bottom:20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            ">
                <h3 style="color:white;">🎵 {row['song']}</h3>
                <p style="color:gray;">👤 {row['artist']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                st.video(row["link"])
            except:
                st.warning("⚠️ Cannot play video here")
                st.markdown(f"[▶️ Watch on YouTube]({row['link']})")
            
            st.write("---")

    
    st.write("### Spotify Recommendations:")

    spotify_songs = search_songs_by_mood(mood)

    if not spotify_songs:
        st.write("⚠️ Spotify temporarily unavailable (using local recommendations only)")
    else:
        for song in spotify_songs:
            st.write(f"**{song['name']}** by {song['artist']}")
            st.write(song["url"])
            st.write("---")