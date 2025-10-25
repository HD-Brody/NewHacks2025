"""Map service (placeholder)

Provides function to convert place names into latitude/longitude pairs.
"""
import os
from dotenv import load_dotenv
import requests

def get_location_coordinates(places, location, country):
    """Return real coordinates for a list of place names.

    Args:
        places (list[str]): Place names
        country (str): Country code (e.g., "US", "CA") that works with ORC

    Returns:
        dict: mapping place -> a dictionaryof dictionaries {location: "The Louvre", coordinates: {'lat': float, 'lng': float}}

    Todo:
        - Integrate with a real geocoding API (Open Route Service API)
        - Cache results
    """
    # Load environment variables from .env file

    # Dynamically determine the path to the .env file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(base_dir, ".env")

    load_dotenv(dotenv_path=dotenv_path)
    api_key = os.getenv("ORS_API_KEY")

    coords = {}
    
    # Simple deterministic mock: hash the place name to a pseudo-lat/lng
    for i, place in enumerate(places or []):

        url = "https://api.openrouteservice.org/geocode/search"

        # determine the focus point depending on index in the list
        if (i == 0):
            params = {
                "api_key": api_key,
                "text": location,
            }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise if status code != 200
            
        data = response.json()
        if data['features']:
            city_lon, city_lat = data['features'][0]['geometry']['coordinates']  

        # get the coordinates using the API
        params = {
            "api_key": api_key,
            "text": place,
            "boundary.country": country,
            "focus.point.lat": city_lat,
            "focus.point.lon": city_lon
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise if status code != 200
            
        data = response.json()
        if data['features']:
            place_lon, place_lat = data['features'][0]['geometry']['coordinates']
        
        coords[place] = {'lat': place_lon, 'lng': place_lat}

    return coords

if __name__ == "__main__":  
    print(os.getenv("ORS_API_KEY"))
    print(get_location_coordinates(["The Louvre", "Musee d'Orsay", "Arc de Triomphe"], "Paris", "FR"))
