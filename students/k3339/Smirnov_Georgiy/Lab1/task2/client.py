import socket  

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9000))
print('Введите катеты через пробел (например: 3 4):')
data = input()
client.send(data.encode())
result = client.recv(1024).decode()
print('Ответ от сервера:', result)
client.close()
