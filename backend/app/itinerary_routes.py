from flask import Blueprint, request, jsonify

from .itinerary_generator import generate_itinerary
from .map_service import get_location_coordinates
from .time_optimizer import optimize_itinerary

itinerary_bp = Blueprint('itinerary', __name__)

@itinerary_bp.route('/generate_itinerary', methods=['POST'])
def generate_itinerary_route():
    """
    POST /api/generate_itinerary
    Body JSON:
    {
        "destination": "Paris",
        "month": "July",
        "preferences": ["food", "museums"]
    }
    """

    data = request.get_json(silent=True) or {}

    destination = data.get('destination')
    month = data.get('month')
    preferences = data.get('preferences', [])

    if not destination:
        return jsonify({'error': 'destination is required'}), 400
    if not month:
        return jsonify({'error': 'month is required'}), 400

    # naive assumptions for now
    budget = "$$"
    category = preferences[0] if preferences else "general"
    country = "FR"  # TODO: infer from destination or user input
    city_name = destination

    # 1. Generate itinerary stops using Gemini
    itinerary = generate_itinerary(destination, month, budget, category)
    # itinerary is like:
    # [
    #   {"name": "place1", "time":[10.30,11.30], "category":"food","price":"$","description":"..."},
    #   ...
    # ]

    # 2. Extract place names
    place_names = [item.get("name") for item in itinerary]

    # 3. Geocode each place
    coords_map = get_location_coordinates(place_names, city_name, country)
    # coords_map is { "place1": {"lat":..., "lng":...}, ... }

    # 4. Attach coordinates to each itinerary item
    for item in itinerary:
        item["coordinates"] = coords_map.get(item["name"])

    # 5. Optionally run optimizer (currently a no-op)
    optimized = optimize_itinerary(itinerary)

    return jsonify({
        'destination': destination,
        'month': month,
        'itinerary': optimized
    })
