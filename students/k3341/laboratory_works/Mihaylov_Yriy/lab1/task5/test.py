import requests

payload1 = {'discipline': "math", 'mark': "5"}
payload2 = {'discipline': "math", 'mark': "2"}
payload3 = {'discipline': "linal", 'mark': "3"}
payload4 = {'discipline': "math", 'mark': "3"}

response_post1 = requests.post("http://127.0.0.1:8080", data=payload1)
print(1)
response_post2 = requests.post("http://127.0.0.1:8080", data=payload2)
print(2)
response_post3 = requests.post("http://127.0.0.1:8080", data=payload3)
print(3)
response_post4 = requests.post("http://127.0.0.1:8080", data=payload4)
print(4)
print(response_post4.text)