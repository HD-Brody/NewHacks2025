import os
import requests 
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
def generate_itinerary(destination: str, month: str, budget: str, category: str) -> list[dict]:
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
    format = "{\"Places\": {\"place1\": { \"time\": [10.30, 11.30], \"category\": \"food\", \"price\": \"$\", \"description\": \"short, clear description\" }, \"place2\": { \"time\": [11.30, 12.00], \"category\": \"store\", \"price\": \"$\", \"description\": \"short, clear description\" }, \"place3\": { \"time\": [12.15, 13.00], \"category\": \"museum\", \"price\": \"$\", \"description\": \"short, clear description\" }, \"place4\": { \"time\": [13.15, 14.00], \"category\": \"outdoor\", \"price\": \"$\", \"description\": \"short, clear description\" } } }"
    prompt = f"You must only respond with a JSON object that gives a daily itinerary for a trip to {destination} based around a given {category} formatted exactly as follows: {format}. Each place in the itinerary must be open and accessible in the specified {month}. Each price must be one of: $, $$, or $$$. Every place must be open at the specified time. Structure the itinerary around the given activity if it is valid. All descriptions must be short, clear, and to the point. Output only JSON, nothing else."
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemini-2.5", 
        "prompt": prompt,
        "max_tokens": 500
    }
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Assume the API returns a JSON list under "result" key
        itinerary = data.get("result", [])

        return itinerary

    except requests.RequestException as e:
        print("Error calling Gemini API:", e)
        # Fallback to sample itinerary
        return [
            { 'place': f'{destination} Old Town', 'start_time': '09:00', 'end_time': '11:00', 'notes': 'Walk historic center' },
            { 'place': f'{destination} Art Museum', 'start_time': '11:30', 'end_time': '13:00', 'notes': 'Local art exhibits' },
            { 'place': f'{destination} Central Park', 'start_time': '14:00', 'end_time': '16:00', 'notes': 'Relax and picnic' },
        ]