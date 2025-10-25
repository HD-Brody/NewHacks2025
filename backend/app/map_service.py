"""Map service (placeholder)

Provides function to convert place names into latitude/longitude pairs. For the
MVP these are mocked values.
"""

def get_location_coordinates(places):
    """Return mock coordinates for a list of place names.

    Args:
        places (list[str]): Place names

    Returns:
        dict: mapping place -> {'lat': float, 'lng': float}

    TODO:
        - Integrate with a real geocoding API (Google Maps, Nominatim, etc.)
        - Cache results
    """
    coords = {}
    # Simple deterministic mock: hash the place name to a pseudo-lat/lng
    for i, place in enumerate(places or []):
        base_lat = 40.0  # arbitrary base
        base_lng = -73.0
        coords[place] = {'lat': base_lat + (i * 0.01), 'lng': base_lng + (i * 0.01)}
    return coords
