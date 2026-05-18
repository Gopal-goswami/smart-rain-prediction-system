def get_nearby_points(lat, lon):

    nearby_points = [

        # North
        (lat + 0.5, lon),

        # South
        (lat - 0.5, lon),

        # East
        (lat, lon + 0.5),

        # West
        (lat, lon - 0.5),

        # North-East
        (lat + 0.5, lon + 0.5),

        # North-West
        (lat + 0.5, lon - 0.5),

        # South-East
        (lat - 0.5, lon + 0.5),

        # South-West
        (lat - 0.5, lon - 0.5)
    ]

    return nearby_points