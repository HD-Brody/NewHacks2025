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
