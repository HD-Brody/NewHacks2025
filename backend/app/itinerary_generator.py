"""Itinerary generator service (placeholder)

This module should contain the logic (or calls to an AI service) to build
an itinerary based on destination, month, and user preferences.
For the MVP we return a hardcoded sample itinerary.
"""

def generate_itinerary(destination, month=None, preferences=None):
    """Return a sample itinerary list for the given destination.

    Args:
        destination (str): Destination name
        month (str|None): Optional month to tailor suggestions
        preferences (list|None): Activity preferences (e.g., ['hiking','museums'])

    Returns:
        list[dict]: List of itinerary items: { place, start_time, end_time, notes }
    TODO:
        - Replace with AI call or smarter generator
        - Respect preferences and month
        - Add durations and categories
    """
    # Simple hardcoded sample. Expand this to call an AI model or DB.
    sample = [
        { 'place': f'{destination} Old Town', 'start_time': '09:00', 'end_time': '11:00', 'notes': 'Walk historic center' },
        { 'place': f'{destination} Art Museum', 'start_time': '11:30', 'end_time': '13:00', 'notes': 'Local art exhibits' },
        { 'place': f'{destination} Central Park', 'start_time': '14:00', 'end_time': '16:00', 'notes': 'Relax and picnic' },
    ]

    # TODO: filter/augment based on preferences
    return sample
