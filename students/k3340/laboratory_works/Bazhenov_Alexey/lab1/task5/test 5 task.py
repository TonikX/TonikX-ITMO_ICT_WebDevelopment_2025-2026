import requests


payload1 = {'discipline': "math", 'mark': "5"}
payload2 = {'discipline': "math", 'mark': "4"}
payload3 = {'discipline': "web", 'mark': "2"}
payload4 = {'discipline': "math", 'mark': "3"}

response_post1 = requests.post("http://127.0.0.1:8080", data=payload1)
response_post2 = requests.post("http://127.0.0.1:8080", data=payload2)
response_post3 = requests.post("http://127.0.0.1:8080", data=payload3)
response_post4 = requests.post("http://127.0.0.1:8080", data=payload4)