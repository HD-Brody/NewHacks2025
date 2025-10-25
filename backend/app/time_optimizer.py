"""Time optimizer placeholder

Contains functions that would reorder or optimize an itinerary based on
distance, opening hours, and user constraints.
"""

def optimize_itinerary(itinerary):
    """Placeholder optimizer that currently returns the itinerary unchanged.

    Args:
        itinerary (list[dict]): List of itinerary items

    Returns:
        list[dict]: Optimized/ordered itinerary

    TODO:
        - Implement simple nearest-neighbor ordering
        - Respect opening/closing hours, durations, user time windows
        - Integrate travel-time estimates (walking/driving)
    """
    # No-op for MVP
    return itinerary
