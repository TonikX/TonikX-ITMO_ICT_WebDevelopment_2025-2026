import socket

# Создаем UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Указываем адрес и порт для сервера
server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Сервер запущен на", server_address)
print("Ожидание сообщений...")

while True:
    # Получаем данные от клиента
    # 1024 - размер буфера для приема данных, если сообщение больше, то только первую часть сообщения будет получена
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    
    print(f"Получено сообщение от {client_address}: {message}")
    
    # Отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), client_address)
    print(f"Отправлен ответ: {response}")
