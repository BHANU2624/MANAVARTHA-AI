import requests
import json
import time
import sys
import os

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def test_conversation():
    print("🚀 Starting Conversational AI Test...")
    
    # 1. Login
    print("🔑 Logging in...")
    login_resp = requests.post(f"{BASE_URL}/auth/login", data={"username": "guest@example.com", "password": "guestpassword123"})
    if login_resp.status_code != 200:
        # Try Guest Login logic or ensure user exists
        # Assuming existing user or guest flow
        # Let's try creating a user if fails or use headers if auth disabled (it is enabled in code)
        # Actually simplest is to disable auth for test or use known creds. 
        # The user provided state shows 'auth_enabled=True'.
        pass 
    
    # Using a fake session ID and mocking user logic if verification fails would take time.
    # Let's use the simplest path: The /search endpoint requires 'current_user'.
    # We'll use the token from login.
    
    token = login_resp.json().get("access_token")
    if not token:
        # Try signup
        print("⚠️ Login failed, trying signup...")
        requests.post(f"{BASE_URL}/auth/signup", json={"email": "testconv@example.com", "password": "password123", "full_name": "Test User"})
        login_resp = requests.post(f"{BASE_URL}/auth/login", data={"username": "testconv@example.com", "password": "password123"})
        token = login_resp.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Authenticated")

    # 2. Turn 1: Initial Query
    query1 = "Telangana rain updates"
    print(f"\n🗣️ User: {query1}")
    resp1 = requests.get(f"{BASE_URL}/search", params={"query": query1}, headers=headers)
    
    if resp1.status_code != 200:
        print(f"❌ Turn 1 Failed: {resp1.status_code} - {resp1.text}")
        return

    data1 = resp1.json()
    session_id = data1.get("session_id")
    # Handle optional answer/fields
    answer1 = data1.get('answer', 'No answer')
    print(f"🤖 Bot: {answer1[:100]}...")
    print(f"🆔 Session ID: {session_id}")
    
    if not session_id:
        print("❌ Session ID missing! Test Failed.")
        return

    print("⏳ Waiting for DB commit...")
    time.sleep(2)

    # 3. Turn 2: Follow-up (Vague)
    query2 = "enduku?"
    print(f"\n🗣️ User: {query2} (Contextual)")
    # Must pass session_id to get context
    resp2 = requests.get(f"{BASE_URL}/search", params={"query": query2, "session_id": session_id}, headers=headers)
    
    if resp2.status_code != 200:
        print(f"❌ Turn 2 Failed: {resp2.status_code} - {resp2.text}")
        return

    data2 = resp2.json()
    answer2 = data2.get('answer', 'No Answer')
    print(f"🤖 Bot: {answer2}")
    
    # Verification
    # If the answer talks about RAIN/WEATHER, it worked.
    # If it says "I don't know what you mean", it failed.
    
    lower_ans = answer2.lower()
    if "varsha" in lower_ans or "rain" in lower_ans or "government" in lower_ans:
        print("\n✅ SUCCESS: Context maintained!")
    else:
        print("\n❌ FAILURE: Context lost.")

if __name__ == "__main__":
    try:
        test_conversation()
    except Exception as e:
        print(f"Error: {e}")
