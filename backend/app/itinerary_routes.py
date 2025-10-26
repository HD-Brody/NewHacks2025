from flask import Blueprint, request, jsonify

from .itinerary_generator import generate_itinerary
from .map_service import get_location_coordinates
from .time_optimizer import optimize_itinerary

itinerary_bp = Blueprint('itinerary', __name__)


@itinerary_bp.route('/generate_itinerary', methods=['POST'])
def generate_itinerary_route():
    """
    POST /api/generate_itinerary
    Expects JSON: { destination: str, month: str, preferences: [str] }

    TODOs:
    - validate input
    - call a real AI itinerary generator or service
    - call map service to get coordinates
    - optimize route/order with time optimizer
    - add caching, rate-limiting, auth as needed
    """
    data = request.get_json(silent=True) or {}
    destination = data.get('destination') or data.get('location')
    month = data.get('month')
    preferences = data.get('preferences', [])
    budget = data.get('budget') or data.get('price')
    # category may be provided explicitly or inferred from preferences
    category = data.get('category') or (preferences[0] if isinstance(preferences, list) and preferences else '')

    # Basic input validation (expand as needed)
    if not destination:
        return jsonify({'error': 'destination is required'}), 400

    # Generate a basic itinerary (placeholder)
    # The generator expects (destination, month, budget, category)
    try:
        itinerary = generate_itinerary(destination, month, budget, category)
    except TypeError:
        # Backwards compatibility: if the generator has a different signature,
        # try calling it with the older (destination, month, preferences) shape.
        itinerary = generate_itinerary(destination, month, preferences)

    # Get mock coordinates for places
    # Build a list of place names from possible keys returned by generator
    places = [item.get('place') or item.get('name') or item.get('title') for item in itinerary]
    coords = get_location_coordinates(places, destination, data.get('country'))

    # Attach coordinates to itinerary items when available
    for item in itinerary:
        key = item.get('place') or item.get('name') or item.get('title')
        item['coordinates'] = coords.get(key)

    # Optionally run an optimizer (placeholder)
    optimized = optimize_itinerary(itinerary)

    return jsonify({'destination': destination, 'month': month, 'itinerary': optimized})

if __name__ == '__main__':
    print(generate_itinerary_route)