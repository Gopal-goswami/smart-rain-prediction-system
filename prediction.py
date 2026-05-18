def predict_rain(weather_data, nearby_weather):

    rain_probability = 0  
  # Humidity Logic
  
    if weather_data["humidity"] > 80:

        rain_probability += 25

    elif weather_data["humidity"] > 60:

        rain_probability += 15

    # Cloud Logic
   
    if weather_data["clouds"] > 80:

        rain_probability += 25

    elif weather_data["clouds"] > 60:

        rain_probability += 15

    # Pressure Logic

    if weather_data["pressure"] < 1000:

        rain_probability += 15

    # Wind Speed Logic
    
    if weather_data["wind_speed"] > 10:

        rain_probability += 10

    # Wind Direction Logic

    wind_direction = weather_data["wind_direction"]

    # Wind coming from North side
    if 300 <= wind_direction <= 360 or 0 <= wind_direction <= 60:

        rain_probability += 10

    # Nearby Rain Logic

    rain_detected = False

    for city in nearby_weather:

        if city["condition"] == "Rain":

            rain_probability += 10

            rain_detected = True


        elif city["condition"] == "Thunderstorm":

            rain_probability += 15

            rain_detected = True

    # Combined Smart Logic

    if rain_detected and weather_data["wind_speed"] > 10:

        rain_probability += 10


    if rain_probability > 100:

        rain_probability = 100


    return rain_probability