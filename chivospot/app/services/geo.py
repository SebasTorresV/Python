from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0


def haversine_distance(
    origin_lat: float,
    origin_lon: float,
    dest_lat: float,
    dest_lon: float,
) -> float:
    """Return the haversine distance in kilometers between two coordinates."""
    lat1, lon1, lat2, lon2 = map(radians, (origin_lat, origin_lon, dest_lat, dest_lon))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return EARTH_RADIUS_KM * c


__all__ = ["haversine_distance", "EARTH_RADIUS_KM"]
