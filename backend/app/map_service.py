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

    # If there's no API key available, return None for every place (dev-friendly)
    if not api_key:
        for place in (places or []):
            coords[place] = None
        return coords

    # Use the OpenRouteService geocode endpoint to find coordinates.
    # Be defensive: external APIs may return empty 'features' and we must not
    # raise unhandled exceptions in the server. For any place we can't resolve,
    # set its value to None so the frontend can handle missing coordinates.
    url = "https://api.openrouteservice.org/geocode/search"

    for i, place in enumerate(places or []):
        city_lon = city_lat = None

        # Try to get a focus point for the requested location (helps geo accuracy)
        if location:
            try:
                params_loc = {"api_key": api_key, "text": location}
                resp = requests.get(url, params=params_loc, timeout=10)
                resp.raise_for_status()
                data = resp.json() or {}
                features = data.get('features') or []
                if features:
                    coords_list = features[0].get('geometry', {}).get('coordinates') or []
                    if len(coords_list) >= 2:
                        city_lon, city_lat = coords_list[0], coords_list[1]
            except Exception as e:
                # Log and continue — don't fail the whole function
                print(f"Warning: failed to fetch focus point for location '{location}': {e}")

        # Now geocode the place itself
        try:
            params_place = {"api_key": api_key, "text": place}
            if country:
                params_place["boundary.country"] = country
            if city_lat is not None and city_lon is not None:
                params_place["focus.point.lat"] = city_lat
                params_place["focus.point.lon"] = city_lon

            resp = requests.get(url, params=params_place, timeout=10)
            resp.raise_for_status()
            data = resp.json() or {}
            features = data.get('features') or []
            if features:
                coords_list = features[0].get('geometry', {}).get('coordinates') or []
                if len(coords_list) >= 2:
                    place_lon, place_lat = coords_list[0], coords_list[1]
                    coords[place] = {'lat': place_lat, 'lng': place_lon}
                else:
                    coords[place] = None
            else:
                coords[place] = None
        except Exception as e:
            print(f"Warning: failed to geocode place '{place}': {e}")
            coords[place] = None

    return coords

def find_path_and_time(start_coords, end_coords, start_time):
    """Return a path and the time it takes given the start and end coordinates

    Args:
        start_coords (dict): {'lat': float, 'lng': float}
        end_coords (dict): {'lat': float, 'lng': float}

    Returns:


    """

    # Load environment variables from .env file

    # Dynamically determine the path to the .env file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(base_dir, ".env")

    load_dotenv(dotenv_path=dotenv_path)
    api_key = os.getenv("TRIPGO_API_KEY")
    
    url = "https://api.tripgo.com/v1/routing.json"

    params = {
            
        }
    headers = {
        "Accept": "application/json", 
        "X-TripGo-Key": api_key

    
    }





if __name__ == "__main__":  
    print(os.getenv("ORS_API_KEY"))
    print(get_location_coordinates(["The Louvre", "Musee d'Orsay", "Arc de Triomphe"], "Paris", "FR"))
