from flask import Blueprint, request, jsonify
from .map_service import get_location_coordinates, find_path_and_time
import traceback

bp = Blueprint('api', __name__)


@bp.route('/geocode', methods=['POST'])
def geocode():
    data = request.get_json() or {}
    places = data.get('places', [])
    location = data.get('location', '')   # city / center point
    country = data.get('country', '')     # optional
    try:
        coords = get_location_coordinates(places, location, country)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        # In dev it's helpful to return the traceback so the frontend can show it.
        return jsonify({'error': str(e), 'traceback': tb}), 500
    return jsonify(coords)


@bp.route('/route_polylines', methods=['POST'])
def route_polylines():
    """Return route polylines between adjacent itinerary items.

    Accepts JSON body in one of two shapes:
      { "itinerary": [ { "coordinates": {"lat": .., "lng": .. }, ... ] }
    or
      { "pairs": [ { "start": {lat,lng}, "end": {lat,lng} }, ... ] }

    Response: list of segment objects:
      [{ "start_index": 0, "end_index": 1,
         "walk": { "duration": seconds, "distance": meters, "polyline": [[lat,lng],...] },
         "car": { ... }
      }, ...]
    """
    data = request.get_json() or {}
    pairs = []
    try:
        if 'pairs' in data and isinstance(data.get('pairs'), list):
            for p in data.get('pairs'):
                s = p.get('start') or {}
                e = p.get('end') or {}
                pairs.append((s, e))
        elif 'itinerary' in data and isinstance(data.get('itinerary'), list):
            itin = data.get('itinerary')
            # build adjacent pairs
            coords_list = []
            for item in itin:
                c = item.get('coordinates') or item.get('coords') or {}
                if c and c.get('lat') is not None and c.get('lng') is not None:
                    coords_list.append({'lat': c.get('lat'), 'lng': c.get('lng')})
                else:
                    coords_list.append(None)
            for i in range(len(coords_list)-1):
                a = coords_list[i]
                b = coords_list[i+1]
                if a and b:
                    pairs.append((a, b))
        else:
            return jsonify({'error': 'Invalid payload, need "itinerary" or "pairs"'}), 400

        results = []
        for idx, (s, e) in enumerate(pairs):
            try:
                # start_time not used for now; pass None or 0
                time_walk, time_car, dist_walk, dist_car, poly_walk, poly_car = find_path_and_time(s, e, None)
                seg = {"start_index": idx, "end_index": idx+1}
                if poly_walk:
                    # poly_walk is expected as list of [lat,lng]
                    seg['walk'] = {"duration": time_walk, "distance": dist_walk, "polyline": poly_walk}
                else:
                    seg['walk'] = None
                if poly_car:
                    seg['car'] = {"duration": time_car, "distance": dist_car, "polyline": poly_car}
                else:
                    seg['car'] = None
            except Exception as e:
                tb = traceback.format_exc()
                print(tb)
                seg = {"start_index": idx, "end_index": idx+1, "error": str(e)}
            results.append(seg)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return jsonify({'error': str(e), 'traceback': tb}), 500

    return jsonify(results)
