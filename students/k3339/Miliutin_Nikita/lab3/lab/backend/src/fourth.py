# fourth.py
import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzY1ODk5NDY0LCJleHAiOjE3NjU5MDMwNjQsInJvbGUiOiJlbXBsb3llZSIsInVzZXJuYW1lIjoibmlraXRhIn0.94d8k34dGxjayawgpFPhHJhYZIaaDefvlgafIZh8NOw"

resp = requests.get(
    f"{BASE_URL}/analytics/chickens-by-breed-and-workshop",
    headers={
        "Authorization": f"Bearer {TOKEN}",
    },
)

print(resp.status_code)
print(resp.json())
