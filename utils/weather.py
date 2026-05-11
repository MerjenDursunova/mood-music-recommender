import requests

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeatherMap API key

def get_weather(city="Seoul"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code != 200:
            print("ERROR:", response.text)
            return None
        
        data = response.json()
        
        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        
        return {
        "weather": weather,
        "temp": temp,
        "feels_like": feels_like,
        "humidity": humidity,
        "pressure": pressure,
        "wind": wind_speed
    }
        
    
    except Exception as e:
        print("EXCEPTION:", e)
        return None


def weather_to_mood(weather):
    weather = weather.lower()
    
    if "rain" in weather:
        return "calm"
    elif "clear" in weather:
        return "happy"
    elif "cloud" in weather:
        return "focused"
    elif "storm" in weather:
        return "energetic"
    else:
        return "calm"