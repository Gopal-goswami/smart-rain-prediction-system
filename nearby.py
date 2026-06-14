import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from distance import calculate_distance


def get_nearby_points(lat, lon):

    points = []

    for dlat in [-1, -0.5, 0, 0.5, 1]:
        for dlon in [-1, -0.5, 0, 0.5, 1]:

            if dlat == 0 and dlon == 0:
                continue

            nearby_lat = lat + dlat
            nearby_lon = lon + dlon

            distance = calculate_distance(
                lat,
                lon,
                nearby_lat,
                nearby_lon
            )

            points.append({
                "lat": nearby_lat,
                "lon": nearby_lon,
                "distance": round(distance, 2)
            })

    return points
