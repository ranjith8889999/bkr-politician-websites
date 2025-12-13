import requests
import json

# API configuration
API_URL = "http://localhost:5000/api/health-camps"
API_KEY = "bkr-secret-key-2025-change-in-production"

# Test data
camp_data = {
    "title": "API Test Camp",
    "date": "2025-12-30",
    "time": "10:00 AM - 4:00 PM",
    "location": "Test Location",
    "services": "Testing",
    "description": "This is a test camp created via API",
    "contact": "+91-1234567890",
    "status": "upcoming"
}

print("=" * 80)
print("Testing Health Camp API Creation")
print("=" * 80)

# Test 1: Create a new health camp
print("\n1. Creating a new health camp...")
try:
    response = requests.post(
        API_URL,
        json=camp_data,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        print("✅ Success! Health camp created.")
    else:
        print("❌ Failed to create health camp.")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get all health camps
print("\n2. Fetching all health camps...")
try:
    response = requests.get(API_URL)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total camps: {data.get('count', 0)}")
    
    if data.get('success'):
        print("✅ Successfully fetched health camps:")
        for camp in data.get('data', []):
            print(f"  - {camp['title']} ({camp['date']})")
    else:
        print("❌ Failed to fetch health camps.")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
