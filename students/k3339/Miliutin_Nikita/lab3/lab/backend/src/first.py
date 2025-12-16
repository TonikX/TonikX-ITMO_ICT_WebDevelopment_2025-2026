import requests
import json

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzY1ODQ2NTQ3LCJleHAiOjE3NjU4NTAxNDcsInJvbGUiOiJlbXBsb3llZSIsInVzZXJuYW1lIjoibmlraXRhIn0.j8MFbxQh6Qrgs2eXouJkbvtdOhrpOVmjEbbQmu7NuQQ"

headers = {"Authorization": f"Bearer {TOKEN}"}

params = {
    "breed_id": 2,
    "min_weight": 1.6,
    "max_weight": 2.0,
    "min_age": 4,
    "max_age": 10,
}

r = requests.get(
    f"{BASE_URL}/analytics/eggs-by-chicken",
    headers=headers,
    params=params,
)

print("Status:", r.status_code)

if r.status_code != 200:
    print(r.text)
else:
    data = r.json()
    print(f"Returned rows: {len(data)}")
    print(json.dumps(data[:5], indent=2, ensure_ascii=False))
