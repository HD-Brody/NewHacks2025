"""Map service (placeholder)

Provides function to convert place names into latitude/longitude pairs.
"""
import os
from dotenv import load_dotenv
import requests
import openrouteservice
import time

def nominatim_lookup(place, city=None):
    """Lookup a place with Nominatim (OpenStreetMap) as a lightweight fallback.

    Returns: {'lat': float, 'lng': float} or None
    """
    try:
        q = f"{place} {city or ''}".strip()
        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "NewHacksDev/1.0 (dev@example.com)"}
        params = {"q": q, "format": "json", "limit": 1}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json() or []
        if not data:
            return None
        first = data[0]
        return {"lat": float(first.get('lat')), "lng": float(first.get('lon'))}
    except Exception as e:
        print(f"Nominatim lookup failed for '{place}': {e}")
        return None

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

        # If ORS returned coordinates, but we had a focus point, ensure the result
        # is reasonably close to the focus (destination). Otherwise, try a
        # re-query with the location appended, and finally fall back to Nominatim.
        def haversine_km(lat1, lon1, lat2, lon2):
            from math import radians, sin, cos, sqrt, atan2
            R = 6371.0
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            return R * c

        too_far = False
        if coords.get(place) and (city_lat is not None and city_lon is not None):
            # Compute distance between city center and discovered place
            p = coords[place]
            try:
                dist_km = haversine_km(city_lat, city_lon, float(p['lat']), float(p['lng']))
                if dist_km > 200:
                    too_far = True
                    print(f"Warning: geocode for '{place}' is {dist_km:.1f}km from focus point; retrying with location context")
            except Exception:
                pass

        if too_far:
            # retry ORS with appended location text
            try:
                params_retry = {"api_key": api_key, "text": f"{place}, {location}"}
                if country:
                    params_retry["boundary.country"] = country
                if city_lat is not None and city_lon is not None:
                    params_retry["focus.point.lat"] = city_lat
                    params_retry["focus.point.lon"] = city_lon
                resp = requests.get(url, params=params_retry, timeout=10)
                resp.raise_for_status()
                data = resp.json() or {}
                features = data.get('features') or []
                if features:
                    coords_list = features[0].get('geometry', {}).get('coordinates') or []
                    if len(coords_list) >= 2:
                        place_lon, place_lat = coords_list[0], coords_list[1]
                        coords[place] = {'lat': place_lat, 'lng': place_lon}
                        # re-check distance
                        try:
                            dist_km = haversine_km(city_lat, city_lon, float(place_lat), float(place_lon))
                            if dist_km > 200:
                                # still far — treat as no result
                                coords[place] = None
                        except Exception:
                            pass
                else:
                    coords[place] = None
            except Exception as e:
                print(f"Warning: retry ORS failed for '{place}': {e}")

        # If ORS didn't return a coordinate (or result was too far), fall back to Nominatim
        if coords.get(place) is None:
            try:
                nomi = nominatim_lookup(place, location)
                if nomi:
                    # if a city focus exists, ensure Nominatim result is not far away
                    if city_lat is not None and city_lon is not None:
                        try:
                            dist_km = haversine_km(city_lat, city_lon, float(nomi['lat']), float(nomi['lng']))
                            if dist_km <= 200:
                                coords[place] = nomi
                        except Exception:
                            coords[place] = nomi
                    else:
                        coords[place] = nomi
                    time.sleep(1)
            except Exception as e:
                print(f"Warning: nominatim fallback failed for '{place}': {e}")

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
    
