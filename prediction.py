def predict_rain(weather_data):

    rain_probability = 0

    humidity = weather_data["humidity"]
    clouds = weather_data["clouds"]
    pressure = weather_data["pressure"]
    wind_speed = weather_data["wind_speed"]
    visibility = weather_data["visibility"]
    condition = weather_data["condition"]


    # HUMIDITY
    if humidity >= 90:
        rain_probability += 30

    elif humidity >= 80:
        rain_probability += 20


    # CLOUDS
    if clouds >= 90:
        rain_probability += 30

    elif clouds >= 70:
        rain_probability += 20


    # PRESSURE
    if pressure < 1000:
        rain_probability += 20


    # CONDITION
    if condition == "Rain":
        rain_probability += 30

    elif condition == "Thunderstorm":
        rain_probability += 40


    # WIND
    if wind_speed > 10:
        rain_probability += 5


    # VISIBILITY
    if visibility < 3000:
        rain_probability += 10


    if rain_probability > 100:
        rain_probability = 100


    return rain_probability