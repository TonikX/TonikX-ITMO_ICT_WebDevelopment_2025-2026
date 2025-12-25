# second.py
import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzY1ODk2NDgzLCJleHAiOjE3NjU5MDAwODMsInJvbGUiOiJlbXBsb3llZSIsInVzZXJuYW1lIjoibmlraXRhIn0.9E0HiE2WSwm13ODgc2FBV-7J_N2uNSuGgJ5G4PO89yA"

resp = requests.get(
    f"{BASE_URL}/analytics/top-workshop-by-breed",
    params={"breed_name": "Hy-Line W-36"},
    headers={"Authorization": f"Bearer {TOKEN}"},
)

print(resp.status_code)
print(resp.json())
