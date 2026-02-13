import requests
import sys

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def test_greeting():
    url = "http://localhost:8000/search"
    
    # Authenticate
    # Authenticate
    auth_url = "http://localhost:8000/auth/login"
    
    email = "greeting_test2@example.com"
    pwd = "password123"
    
    signup_payload = {
        "email": email,
        "password": pwd,
        "full_name": "Greeting Tester"
    }
    
    # Try signup
    reg_url = "http://localhost:8000/auth/signup"
    try:
         requests.post(reg_url, json=signup_payload)
    except:
         pass

    # Login (Form Data)
    login_data = {
        "username": email,
        "password": pwd
    }
    
    sess = requests.Session()
    resp = sess.post(auth_url, data=login_data)
    
    token = None
    if resp.status_code == 200:
        token = resp.json().get("access_token")
    else:
        print(f"Login failed: {resp.text}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    # Test Greeting
    print("👋 Testing Greeting (Should be FAST)...")
    try:
        r = requests.get(url, params={"query": "namaste", "mode": "standard"}, headers=headers)
        if r.status_code == 200:
            data = r.json()
            ans = data['answer']
            if "మనవార్త" in ans:
                print("✅ Greeting Success: " + ans)
            else:
                print("❌ Greeting Content Mismatch: " + ans)
        else:
            print(f"❌ Greeting Failed: {r.status_code}")
            print(f"Server Response: {r.text}")
    except Exception as e:
        print(f"❌ Greeting Error: {e}")

if __name__ == "__main__":
    test_greeting()
