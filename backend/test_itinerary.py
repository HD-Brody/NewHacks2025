import requests
import json

def test_generate_itinerary():
    url = 'http://127.0.0.1:5000/api/generate_itinerary'
    
    # Test case 1: Valid input
    payload = {
        'destination': 'Toronto',
        'month': 'October',
        'preferences': ['food', 'culture', 'outdoor']
    }
    
    print("\nTest 1: Valid input")
    print(f"Sending: {json.dumps(payload, indent=2)}")
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test case 2: Missing required field
    payload_missing = {
        'month': 'October',
        'preferences': ['food']
    }
    
    print("\nTest 2: Missing destination")
    print(f"Sending: {json.dumps(payload_missing, indent=2)}")
    response = requests.post(url, json=payload_missing)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == '__main__':
    test_generate_itinerary()