from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from arrival_time import calculate_arrival_time
from nearby import get_nearby_points
from typing import Optional

from weather import (
    get_hourly_forecast,
    get_weather,
    get_weather_by_coords,
    get_10_day_forecast,
    get_aqi
)

from prediction import predict_rain

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# ======================================
# HOME PAGE
# ======================================

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )


# ======================================
# WEATHER INFO
# ======================================

@app.get("/dashboard")
async def dashboard(request: Request,  lat: float, lon: float):

    weather_data = get_weather(lat, lon)
    hourly_forecast = get_hourly_forecast(lat, lon)
    forecast = get_10_day_forecast(lat, lon)
    aqi_data = get_aqi(lat, lon)

    rain_conditions = [
        "Rain",
        "Drizzle",
        "Thunderstorm"
    ]

    current_city_raining = (
        weather_data.get("condition") in rain_conditions
    )

    nearest_rain = None
    arrival_time = None
    confidence = "Low"
    top_rain_locations = []

    nearby_weather = []

    if not current_city_raining:

        nearby_points = get_nearby_points(lat, lon)

        for point in nearby_points:

            data = get_weather_by_coords(
                point["lat"],
                point["lon"]
            )


            # Rain ya strong cloud system detect
            if (data.get("condition") in rain_conditions or data.get("clouds", 0) > 85 or data.get("humidity", 0) > 80):

                data["distance"] = point["distance"]

                nearby_weather.append(data)


        if nearby_weather:

            nearby_weather.sort(
                key=lambda x: x.get("distance", 0)
            )

            nearest_rain = nearby_weather[0]
            top_rain_locations = nearby_weather[1:6]

            arrival_time = calculate_arrival_time(
                nearest_rain.get("distance", 0),
                nearest_rain.get("wind_speed", 0)
            )

            if nearest_rain["condition"] in rain_conditions:
                confidence = "High"

            elif nearest_rain["clouds"] > 90:
                confidence = "Medium"

            else:
                confidence = "Low"

            if arrival_time is not None and arrival_time <= 30:
                confidence = "High" 

    rain_probability = predict_rain(
        weather_data,
        nearest_rain
    )

    weather_data["rain_probability"] = rain_probability

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "weather": weather_data,
            "hourly_forecast": hourly_forecast,
            "forecast": forecast,
            "aqi": aqi_data,
            "rain_probability": rain_probability,
            "nearest_rain": nearest_rain,
            "arrival_time": arrival_time,
            "confidence": confidence,
            "top_rain_locations": top_rain_locations,
            "lat": lat,
            "lon": lon
        }
    )

