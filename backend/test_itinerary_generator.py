import json
from app.itinerary_generator import generate_itinerary


def main():
    # Hardcoded test parameters
    destination = "Japan"
    month = "October"
    budget = "$$"
    category = "food"

    print(f"Calling generate_itinerary(destination={destination!r}, month={month!r}, budget={budget!r}, category={category!r})")

    itinerary = generate_itinerary(destination, month, budget, category)

    # Pretty-print the result
    try:
        print(json.dumps(itinerary, indent=2, ensure_ascii=False))
    except TypeError:
        # If the returned object is not JSON-serializable, print raw
        print(itinerary)


if __name__ == '__main__':
    main()
