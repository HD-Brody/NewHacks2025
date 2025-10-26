"""Map service (placeholder)

Provides function to convert place names into latitude/longitude pairs.
"""
import os
from dotenv import load_dotenv
import requests
try:
    import openrouteservice
except Exception:
    openrouteservice = None
    print('Warning: optional dependency "openrouteservice" not installed; route decoding will be limited.')
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

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

    def haversine_km(lat1, lon1, lat2, lon2):
        from math import radians, sin, cos, sqrt, atan2
        R = 6371.0
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c

    # load or initialize on-disk cache
    try:
        cache_file = Path(base_dir) / 'geocode_cache.json'
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as fh:
                cache = json.load(fh)
        else:
            cache = {}
    except Exception:
        cache = {}

    # helper to persist cache (best-effort)
    def _save_cache():
        try:
            with open(Path(base_dir) / 'geocode_cache.json', 'w', encoding='utf-8') as fh:
                json.dump(cache, fh)
        except Exception:
            pass

    # If there's no API key available, we'll still try Nominatim in parallel
    url = "https://api.openrouteservice.org/geocode/search"

    # gather list of places to resolve
    places_list = list(places or [])
    # preload cache hits
    for place in places_list:
        if place in cache:
            coords[place] = cache.get(place)
        else:
            coords[place] = None

    # quick helper for a single place resolution (uses ORS -> retry -> nominatim)
    def _resolve_place(place):
        # if cache hit, return immediately
        if place in cache and cache.get(place) is not None:
            return place, cache.get(place)

        city_lon = city_lat = None
        if location:
            try:
                params_loc = {"api_key": api_key, "text": location} if api_key else {"text": location}
                resp = requests.get(url, params=params_loc, timeout=8)
                resp.raise_for_status()
                data = resp.json() or {}
                features = data.get('features') or []
                if features:
                    coords_list = features[0].get('geometry', {}).get('coordinates') or []
                    if len(coords_list) >= 2:
                        city_lon, city_lat = coords_list[0], coords_list[1]
            except Exception:
                city_lon = city_lat = None

        # define a small inner lookup to call ORS and pick closest feature
        def _call_ors(query_text):
            try:
                params = {"api_key": api_key, "text": query_text} if api_key else {"text": query_text}
                if country:
                    params["boundary.country"] = country
                if city_lat is not None and city_lon is not None:
                    params["focus.point.lat"] = city_lat
                    params["focus.point.lon"] = city_lon
                resp = requests.get(url, params=params, timeout=8)
                resp.raise_for_status()
                data = resp.json() or {}
                features = data.get('features') or []
                if not features:
                    return None
                # pick closest to city focus if available
                if city_lat is not None and city_lon is not None:
                    best = None
                    best_dist = None
                    for f in features:
                        coords_list = f.get('geometry', {}).get('coordinates') or []
                        if len(coords_list) < 2:
                            continue
                        lon, lat = coords_list[0], coords_list[1]
                        try:
                            dist_km = haversine_km(city_lat, city_lon, float(lat), float(lon))
                        except Exception:
                            dist_km = None
                        if best is None or (dist_km is not None and (best_dist is None or dist_km < best_dist)):
                            best = (lon, lat)
                            best_dist = dist_km
                    if best is not None:
                        place_lon, place_lat = best[0], best[1]
                        # if best is too far, treat as no result
                        if best_dist is not None and best_dist > 200:
                            return None
                        return {'lat': place_lat, 'lng': place_lon}
                # fallback to first feature
                coords_list = features[0].get('geometry', {}).get('coordinates') or []
                if len(coords_list) >= 2:
                    place_lon, place_lat = coords_list[0], coords_list[1]
                    return {'lat': place_lat, 'lng': place_lon}
            except Exception:
                return None

        # try ORS with appended location (if available)
        q = f"{place}, {location}" if location else place
        res = None
        if api_key:
            res = _call_ors(q)
        # if ORS not available or returned None, try nominatim
        if res is None:
            try:
                nomi = nominatim_lookup(place, location)
                if nomi:
                    res = nomi
            except Exception:
                res = None

        # save to cache for future
        try:
            cache[place] = res
        except Exception:
            pass
        return place, res

    # run resolves in parallel for missing places
    to_resolve = [p for p in places_list if coords.get(p) is None]
    if to_resolve:
        with ThreadPoolExecutor(max_workers=min(8, max(2, len(to_resolve)))) as ex:
            futures = {ex.submit(_resolve_place, p): p for p in to_resolve}
            for fut in as_completed(futures):
                try:
                    p, r = fut.result()
                    coords[p] = r
                except Exception:
                    coords[futures[fut]] = None

        # persist cache (best-effort)
        _save_cache()

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

    # Defaults in case routes are missing
    time_walk = time_car = None
    distance_walk = distance_car = None
    polyline_decodedl_walk = polyline_decodedl_car = None

    if data_walk.get('routes'):
        time_walk = data_walk['routes'][0]['summary'].get('duration')
        distance_walk = data_walk['routes'][0]['summary'].get('distance')
        polyline_walk = data_walk['routes'][0].get('geometry')
        # decode polyline only if openrouteservice is available
        if openrouteservice and polyline_walk:
            try:
                decoded_walk = openrouteservice.convert.decode_polyline(polyline_walk)
                polyline_decoded_walk = decoded_walk.get('coordinates')
                if polyline_decoded_walk:
                    polyline_decodedl_walk = [[lat, lon] for lon, lat in polyline_decoded_walk]
            except Exception:
                polyline_decodedl_walk = None

    if data_car.get('routes'):
        time_car = data_car['routes'][0]['summary'].get('duration')
        distance_car = data_car['routes'][0]['summary'].get('distance')
        polyline_car = data_car['routes'][0].get('geometry')
        if openrouteservice and polyline_car:
            try:
                decoded_car = openrouteservice.convert.decode_polyline(polyline_car)
                polyline_decoded_car = decoded_car.get('coordinates')
                if polyline_decoded_car:
                    polyline_decodedl_car = [[lat, lon] for lon, lat in polyline_decoded_car]
            except Exception:
                polyline_decodedl_car = None

    return time_walk, time_car, distance_walk, distance_car, polyline_decodedl_walk, polyline_decodedl_car

if __name__ == "__main__":  
    print(os.getenv("ORS_API_KEY"))
    print(get_location_coordinates(["The Louvre", "Musee d'Orsay", "Arc de Triomphe"], "Paris", "FR"))

    # the louvre
    # arc de triomphe
    print(find_path_and_time({'lng': 2.3364, 'lat': 48.8606}, {'lng': 2.295, 'lat': 48.8738}, 1761433377))
    
