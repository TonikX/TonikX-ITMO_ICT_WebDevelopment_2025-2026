import requests

BASE_URL = "http://localhost:8000"

r = requests.post(
    f"{BASE_URL}/auth/token",
    data={
        "username": "nikita",
        "password": "12345678",
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)

print("STATUS:", r.status_code)
print("TEXT:", r.text)
