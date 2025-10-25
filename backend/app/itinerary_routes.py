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
    destination = data.get('destination')
    month = data.get('month')
    preferences = data.get('preferences', [])

    # Basic input validation (expand as needed)
    if not destination:
        return jsonify({'error': 'destination is required'}), 400

    # Generate a basic itinerary (placeholder)
    itinerary = generate_itinerary(destination, month, preferences)

    # Get mock coordinates for places
    places = [item.get('place') for item in itinerary]
    coords = get_location_coordinates(places)

    # Attach coordinates to itinerary items when available
    for item in itinerary:
        item['coordinates'] = coords.get(item.get('place'))

    # Optionally run an optimizer (placeholder)
    optimized = optimize_itinerary(itinerary)

    return jsonify({'destination': destination, 'month': month, 'itinerary': optimized})
