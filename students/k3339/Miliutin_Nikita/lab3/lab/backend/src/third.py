# third.py
import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzY1ODk2NDgzLCJleHAiOjE3NjU5MDAwODMsInJvbGUiOiJlbXBsb3llZSIsInVzZXJuYW1lIjoibmlraXRhIn0.9E0HiE2WSwm13ODgc2FBV-7J_N2uNSuGgJ5G4PO89yA"

r = requests.get(
    f"{BASE_URL}/analytics/eggs-per-employee-per-day",
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=10,
)
r.raise_for_status()
print(r.json())
