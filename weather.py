import os
import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}"
        f"&lon={lon}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    local_dt = datetime.datetime.utcfromtimestamp(
        data["dt"] + data.get("timezone", 0)
    )

    return {
        "city": data["name"],

        "temperature": data["main"]["temp"],

        "feels_like": data["main"]["feels_like"],

        "humidity": data["main"]["humidity"],

        "pressure": data["main"]["pressure"],

        "clouds": data["clouds"]["all"],

        "wind_speed": round(data["wind"]["speed"] * 3.6, 2),

        "wind_direction": data["wind"]["deg"],

        "visibility": data["visibility"],

        "condition": data["weather"][0]["main"],

        "description": data["weather"][0]["description"],

        "lat": data["coord"]["lat"],

        "lon": data["coord"]["lon"],

        "icon": (
            f"https://openweathermap.org/img/wn/"
            f"{data['weather'][0]['icon']}@4x.png"
        ),

        "date": local_dt.strftime("%d %b %Y"),

        "time": local_dt.strftime("%I:%M %p")
    }


def get_weather_by_coords(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}"
        f"&lon={lon}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    return {

        "city": data["name"],

        "temperature": data["main"]["temp"],

        "humidity": data["main"]["humidity"],

        "clouds": data["clouds"]["all"],

        "wind_speed": round(data["wind"]["speed"] * 3.6, 2),

        "wind_direction": data["wind"]["deg"],

        "condition": data["weather"][0]["main"],

        "lat": data["coord"]["lat"],

        "lon": data["coord"]["lon"]
    }


def get_hourly_forecast(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}"
        f"&lon={lon}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    forecast_data = []

    for item in data["list"][:8]:

        icon_code = item["weather"][0]["icon"]

        formatted_time = datetime.datetime.strptime(
            item["dt_txt"],
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%I:%M %p")

        forecast_data.append({

            "time": formatted_time,

            "temp": round(item["main"]["temp"]),

            "feels_like": round(item["main"]["feels_like"]),

            "humidity": item["main"]["humidity"],

            "clouds": item["clouds"]["all"],

            "wind_speed": item["wind"]["speed"],

            "condition": item["weather"][0]["main"],

            "icon": (
                f"https://openweathermap.org/img/wn/"
                f"{icon_code}@4x.png"
            ),

            "rain_probability": round(
                item.get("pop", 0) * 100
            )
        })

    return forecast_data


def get_10_day_forecast(lat, lon):

    url = (
        f"http://api.weatherapi.com/v1/forecast.json?"
        f"key={WEATHER_API_KEY}"
        f"&q={lat},{lon}"
        f"&days=10"
        f"&aqi=no"
        f"&alerts=no"
    )

    response = requests.get(url)
    data = response.json()

    forecast_days = []

    for day in data["forecast"]["forecastday"]:

        forecast_days.append({

            "date": day["date"],

            "max_temp": round(day["day"]["maxtemp_c"]),

            "min_temp": round(day["day"]["mintemp_c"]),

            "condition": day["day"]["condition"]["text"],

            "icon": "https:" + day["day"]["condition"]["icon"],

            "rain_probability": day["day"]["daily_chance_of_rain"],

            "humidity": day["day"]["avghumidity"],

            "wind_speed": day["day"]["maxwind_kph"]
        })

    return forecast_days


def get_aqi(lat, lon):

    url = (
        f"https://api.weatherapi.com/v1/current.json"
        f"?key={WEATHER_API_KEY}"
        f"&q={lat},{lon}"
        f"&aqi=yes"
    )

    response = requests.get(url)
    data = response.json()

    aqi = data["current"]["air_quality"]["us-epa-index"]

    status_map = {
        1: "Good",
        2: "Moderate",
        3: "Unhealthy for Sensitive Groups",
        4: "Unhealthy",
        5: "Very Unhealthy",
        6: "Hazardous"
    }

    return {
        "aqi": aqi,
        "status": status_map.get(aqi, "Unknown")
    }



