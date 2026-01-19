import requests
grades = {"Math": "3", "Web": 3}
url = "http://127.0.0.1:8123"


response = requests.post(url, params=grades, timeout=5)

print("Статус:", response.status_code)
print("Ответ:", response.text)