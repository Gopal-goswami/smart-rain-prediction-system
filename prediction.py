def predict_rain(weather, nearest_rain=None):

    probability = 0


    # =========================
    # HUMIDITY
    # =========================

    if weather["humidity"] > 80:

        probability += 35

    elif weather["humidity"] > 60:

        probability += 20


    # =========================
    # CLOUDS
    # =========================

    if weather["clouds"] > 80:

        probability += 30

    elif weather["clouds"] > 60:

        probability += 15


    # =========================
    # CURRENT WEATHER CONDITION
    # =========================

    if weather["condition"] in [

        "Rain",

        "Drizzle",

        "Thunderstorm"
    ]:

        probability += 40


    # =========================
    # WIND SPEED
    # =========================

    if weather["wind_speed"] > 15:

        probability += 10


    # =========================
    # NEARBY RAIN EFFECT
    # =========================

    if nearest_rain:

        probability += 20


    # =========================
    # LIMIT MAX 100
    # =========================

    probability = min(probability, 100)


    return probability