import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    try:
        print(f"Testing {BASE_URL}/health ...")
        r = requests.get(f"{BASE_URL}/health")
        if r.status_code == 200:
            print("✅ Health Check Passed")
            print(json.dumps(r.json(), indent=2))
            return True
        else:
            print(f"❌ Health Check Failed: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

def test_search():
    try:
        print(f"\nTesting {BASE_URL}/search ...")
        # Query for 'cricket', simulating a user
        r = requests.get(f"{BASE_URL}/search", params={"query": "cricket"})
        if r.status_code == 200:
            print("✅ Search Check Passed")
            data = r.json()
            print(f"Answer: {data.get('answer')}")
            print(f"Sources: {len(data.get('sources', []))}")
            return True
        else:
            print(f"❌ Search Check Failed: {r.status_code}")
            print(r.text)
            return False
    except Exception as e:
        print(f"❌ Search Check Error: {e}")
        return False

if __name__ == "__main__":
    health = test_health()
    search = test_search()
    
    if health and search:
        print("\n🎉 ALL CHECKS PASSED")
        sys.exit(0)
    else:
        print("\n⚠️ SOME CHECKS FAILED")
        sys.exit(1)
