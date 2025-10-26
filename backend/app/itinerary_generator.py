import os
import requests
import json
import re
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
        '"name_of_place1": { "time": [10:30, 11:30], "category": "food", "price": "$", "description": "short, clear description" }, '
        '"name_of_place2": { "time": [11:30, 12:00], "category": "store", "price": "$", "description": "short, clear description" }, '
        '"name_of_place3": { "time": [12:15, 13:00], "category": "museum", "price": "$", "description": "short, clear description" }, '
        '"name_of_place4": { "time": [13:15, 14:00], "category": "outdoor", "price": "$", "description": "short, clear description" } } }'
    )

    prompt = (
        f"""
        You must only respond with a JSON object that gives a daily itinerary for a trip to {destination},
        based around a given {category} activity with a **{budget}** price point, formatted exactly as follows: {format_template}.

        Each "place" in the itinerary must meet ALL of the following **strict** requirements:

        1. The "name" field must contain the official, mappable name of the business, attraction, or landmark exactly as it appears in OpenStreetMap or Google Maps (the primary listing name).
        2. If the primary listing name by itself is ambiguous or would likely return multiple geocoding results, append the **minimal disambiguator** in parentheses directly after the name. The minimal disambiguator should be, in order of preference:
        a) full street address in the format "Street number Street name, City, Country"  
        b) otherwise "City, Country"  
        c) otherwise the well-known neighborhood only if essential for disambiguation.
        Example:  
            - `Trattoria Da Enzo`  (if unambiguous)  
            - `Trattoria Da Enzo (Via dei Vascellari 29, Rome, Italy)`  (if needed to disambiguate)  
            - `Tokyo Sushi Academy (Tsukiji, Tokyo, Japan)`  (only if address not available)
        3. **Do not** invent marketing suffixes or branch labels that are not part of the map listing (avoid "al 29", "Tsukiji" appended to the brand unless that exact phrase appears in the map entry).
        4. Use the map's canonical capitalization, punctuation, and diacritics when possible (e.g., "Café" not "Cafe")—but do not add extra words.
        5. If the official listing includes a suite/branch name as part of the map entry, include it exactly; otherwise omit branch or neighborhood tokens.
        6. Each place must be open and accessible in {month}.
        7. Each place must be within a reasonable travel distance so the full day’s itinerary is visitable in one day.
        8. Prices must be $, $$, or $$$.
        9. Time values must be strings in 24-hour format `"HH:MM"` (for example, `"10:15"`).
        10. Descriptions must be short, clear, and to the point.
        11. Output only valid JSON exactly matching the provided structure — no extra text, no commentary.

        If you cannot find a single unambiguous map name for a place that fits the activity, prefer a different place rather than inventing or guessing a name.
        """
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

        # Try direct JSON parse first, then attempt to clean common wrappers
        full_itinerary_dict = None
        try:
            full_itinerary_dict = json.loads(itinerary_text)
        except json.JSONDecodeError:
            # Common model outputs include markdown fences or extra text. Try to
            # extract the first JSON object found in the string.
            cleaned = itinerary_text
            # remove Markdown code fences (```json ... ```)
            cleaned = re.sub(r"```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\s*```\s*$", "", cleaned)
            # Try to find the first {...} JSON object in the text
            m = re.search(r"(\{.*\})", cleaned, flags=re.DOTALL)
            if m:
                candidate = m.group(1)
                try:
                    full_itinerary_dict = json.loads(candidate)
                except json.JSONDecodeError:
                    full_itinerary_dict = None

        if not full_itinerary_dict:
            print("Could not parse model output as JSON:")
            print(itinerary_text)
            return []

        # Convert the dictionary to a list to match the return type hint
        places_dict = full_itinerary_dict.get("Places", {})
        itinerary_list = []
        for name, details in places_dict.items():
            place_data = {"name": name}
            place_data.update(details)
            itinerary_list.append(place_data)

        return itinerary_list

    except Exception as e:
        print("Error calling Gemini API:", e)
        # Fallback to sample itinerary
        return [
            {'place': f'{destination} Old Town', 'start_time': '09:00', 'end_time': '11:00', 'notes': 'Walk historic center'},
            {'place': f'{destination} Art Museum', 'start_time': '11:30', 'end_time': '13:00', 'notes': 'Local art exhibits'},
            {'place': f'{destination} Central Park', 'start_time': '14:00', 'end_time': '16:00', 'notes': 'Relax and picnic'},
        ]