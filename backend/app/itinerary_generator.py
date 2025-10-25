import os
import requests
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)
# Get API key from env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Use the v1beta2 generate endpoint (use :generate suffix)
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5-flash:generate"

def generate_itinerary(destination: str, month: str, budget: str, category: str) -> list[dict]:
    # Use single quotes for the internal keys to simplify the outer string escaping
    format_template = (
        '{"Places": {'
        '"place1": { "time": [10.30, 11.30], "category": "food", "price": "$", "description": "short, clear description" }, '
        '"place2": { "time": [11.30, 12.00], "category": "store", "price": "$", "description": "short, clear description" }, '
        '"place3": { "time": [12.15, 13.00], "category": "museum", "price": "$", "description": "short, clear description" }, '
        '"place4": { "time": [13.15, 14.00], "category": "outdoor", "price": "$", "description": "short, clear description" } } }'
    )

    prompt = (
        f"You must only respond with a JSON object that gives a daily itinerary for a trip to {destination} "
        f"based around a given {category} activity with a **{budget}** price point, formatted exactly as follows: {format_template}. "
        f"Each place in the itinerary must be open and accessible in {month}. "
        f"Each price must be $, $$, or $$$. Every place must be open at the specified time. "
        f"Structure the itinerary around the given activity. All descriptions must be short, clear, and to the point. "
        f"Output only JSON, nothing else."
    )

    # Use only Content-Type header; pass API key as query parameter if available
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        # Ideally, add the response_mime_type and response_schema here for robustness
    }

    try:
        # Use the official google.generativeai client library to call Gemini.
        # Configure the client if an API key is available.
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(model_name="gemini-2.5-flash")

        # Generate content with the prompt. The client returns an object with a .text property.
        response = model.generate_content(prompt)
        itinerary_text = (getattr(response, "text", "") or str(response)).strip()

        try:
            full_itinerary_dict = json.loads(itinerary_text)

            # Convert the dictionary to a list to match the return type hint
            places_dict = full_itinerary_dict.get("Places", {})
            itinerary_list = []
            for name, details in places_dict.items():
                place_data = {"name": name}
                place_data.update(details)
                itinerary_list.append(place_data)

            return itinerary_list

        except json.JSONDecodeError:
            print("Could not parse model output as JSON:")
            print(itinerary_text)
            return []

    except Exception as e:
        print("Error calling Gemini API:", e)
        # Fallback to sample itinerary
        return [
            {'place': f'{destination} Old Town', 'start_time': '09:00', 'end_time': '11:00', 'notes': 'Walk historic center'},
            {'place': f'{destination} Art Museum', 'start_time': '11:30', 'end_time': '13:00', 'notes': 'Local art exhibits'},
            {'place': f'{destination} Central Park', 'start_time': '14:00', 'end_time': '16:00', 'notes': 'Relax and picnic'},
        ]