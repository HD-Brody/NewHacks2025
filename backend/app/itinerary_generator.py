import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# we'll just use the client lib, not raw requests
MODEL_NAME = "gemini-2.5-flash"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_itinerary(destination: str, month: str, budget: str, category: str) -> list[dict]:
    """
    Return a list of places in the day, each like:
    {
        "name": "place1",
        "time": [10.30, 11.30],
        "category": "food",
        "price": "$",
        "description": "short, clear description"
    }
    """

    format_template = (
        '{"Places": {'
        '"place1": { "time": [10.30, 11.30], "category": "food", "price": "$", "description": "short, clear description" }, '
        '"place2": { "time": [11.30, 12.00], "category": "store", "price": "$", "description": "short, clear description" }, '
        '"place3": { "time": [12.15, 13.00], "category": "museum", "price": "$", "description": "short, clear description" }, '
        '"place4": { "time": [13.15, 14.00], "category": "outdoor", "price": "$", "description": "short, clear description" } } }'
    )

    prompt = (
        f"You must only respond with a JSON object that gives a daily itinerary for a trip to {destination} "
        f"based around a given {category} activity with a {budget} price point, formatted exactly as follows: {format_template}. "
        f"Each place in the itinerary must be open and accessible in {month}. "
        f"Each price must be $, $$, or $$$. Every place must be open at the specified time. "
        f"Structure the itinerary around the given activity. All descriptions must be short, clear, and to the point. "
        f"Output only JSON, nothing else."
    )

    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        itinerary_text = (getattr(response, "text", "") or str(response)).strip()

        try:
            full_itinerary_dict = json.loads(itinerary_text)
        except json.JSONDecodeError:
            print("[generate_itinerary] Could not parse model output as JSON:")
            print(itinerary_text)
            raise RuntimeError("Model did not return valid JSON")

        places_dict = full_itinerary_dict.get("Places", {})
        itinerary_list = []
        for name, details in places_dict.items():
            place_data = {"name": name}
            place_data.update(details)
            itinerary_list.append(place_data)

        return itinerary_list

    except Exception as e:
        print("[generate_itinerary] Error calling Gemini or parsing:", e)

        # Fallback: SAME SHAPE AS SUCCESS PATH (critical!)
        return [
            {
                "name": "place1",
                "time": [9.00, 11.00],
                "category": "walk",
                "price": "$",
                "description": f"Walk historic {destination} center"
            },
            {
                "name": "place2",
                "time": [11.30, 13.00],
                "category": "museum",
                "price": "$$",
                "description": f"Explore local art in {destination}"
            },
            {
                "name": "place3",
                "time": [14.00, 16.00],
                "category": "park",
                "price": "$",
                "description": "Relax outdoors and grab a snack"
            },
        ]
