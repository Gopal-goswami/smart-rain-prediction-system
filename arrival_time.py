def calculate_arrival_time(distance, wind_speed):

    if wind_speed <= 0:
        return None

    return round((distance / wind_speed) / 60)