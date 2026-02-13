import requests
import json

url = "http://127.0.0.1:8000/auth/signup"
payload = {
    "email": "testuser@example.com",
    "password": "password123",
    "full_name": "Test User"
}
headers = {'Content-Type': 'application/json'}

try:
    print(f"Sending POST to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"FULL ERROR: {data}")
    except:
        print(f"Raw Body: {response.text}")
except Exception as e:
    print(f"Request Failed: {e}")
