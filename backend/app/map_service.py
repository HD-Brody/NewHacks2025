"""Map service (placeholder)

Provides function to convert place names into latitude/longitude pairs.
"""
import os
from dotenv import load_dotenv
import requests
import openrouteservice

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

def find_path_and_time(start_coords, end_coords, start_time):
    """Return a path and the time it takes given the start and end coordinates

    Args:
        start_coords (dict): {'lat': float, 'lng': float}
        end_coords (dict): {'lat': float, 'lng': float}
        start_time: time after 1970 in seconds

    Returns:
    """

    # Load environment variables from .env file

    # Dynamically determine the path to the .env file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(base_dir, ".env")

    load_dotenv(dotenv_path=dotenv_path)
    api_key = os.getenv("ORS_API_KEY")
    
    url_walk = "https://api.openrouteservice.org/v2/directions/foot-walking/json"
    url_car = "https://api.openrouteservice.org/v2/directions/driving-car/json"

    body = {
        "coordinates": [[start_coords['lng'], start_coords['lat']], [end_coords['lng'], end_coords['lat']]],
    }
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': api_key,
    'Content-Type': 'application/json; charset=utf-8'
    }

    response_walk = requests.post(url_walk, json=body, headers=headers)
    response_walk.raise_for_status()  # Raise if status code != 200
    data_walk = response_walk.json()

    response_car = requests.post(url_car, json=body, headers=headers)
    response_car.raise_for_status()  # Raise if status code != 200
    data_car = response_car.json()

    if data_walk['routes']:
        time_walk = data_walk['routes'][0]['summary']['duration']
        distance_walk = data_walk['routes'][0]['summary']['distance']
        polyline_walk = data_walk['routes'][0]['geometry']
        client_walk = openrouteservice.Client(key=api_key)
        decoded_walk = openrouteservice.convert.decode_polyline(polyline_walk)
        polyline_decoded_walk = decoded_walk['coordinates']
        polyline_decodedl_walk = [[lat, lon] for lon, lat in polyline_decoded_walk]


    if data_car['routes']:
        time_car = data_car['routes'][0]['summary']['duration']
        distance_car = data_car['routes'][0]['summary']['distance']
        polyline_car = data_car['routes'][0]['geometry']
        client_car = openrouteservice.Client(key=api_key)
        decoded_car = openrouteservice.convert.decode_polyline(polyline_car)
        polyline_decoded_car = decoded_car['coordinates']
        polyline_decodedl_car = [[lat, lon] for lon, lat in polyline_decoded_car]

    return time_walk, time_car, distance_walk, distance_car, polyline_decodedl_walk, polyline_decodedl_car

if __name__ == "__main__":  
    print(os.getenv("ORS_API_KEY"))
    print(get_location_coordinates(["The Louvre", "Musee d'Orsay", "Arc de Triomphe"], "Paris", "FR"))

    # the louvre
    # arc de triomphe
    print(find_path_and_time({'lng': 2.3364, 'lat': 48.8606}, {'lng': 2.295, 'lat': 48.8738}, 1761433377))
    
