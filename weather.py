import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data=response.json()
    return {
        "city": city,

        "temperature": data["main"]["temp"],

        "feels_like": data["main"]["feels_like"],

        "humidity": data["main"]["humidity"],

        "pressure": data["main"]["pressure"],

        "clouds": data["clouds"]["all"],

        "wind_speed": data["wind"]["speed"],

        "wind_direction": data["wind"]["deg"],

        "visibility": data["visibility"],

        "condition": data["weather"][0]["main"],

        "description": data["weather"][0]["description"]
    }

