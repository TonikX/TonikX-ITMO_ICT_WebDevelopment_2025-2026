import requests

BASE_URL = "http://127.0.0.1:8000"  # поменяй если у тебя другой хост/порт
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzY1OTAyNzM3LCJleHAiOjE3NjU5MDYzMzcsInJvbGUiOiJlbXBsb3llZSIsInVzZXJuYW1lIjoibmlraXRhIn0.fei4K7vZBilTJR9mBDmcS_orUAPiiQ6Sm32uXK5OZnY"

r = requests.get(
    f"{BASE_URL}/analytics/breed-eggs-delta",
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=10,
)
print("status:", r.status_code)
print(r.json())
