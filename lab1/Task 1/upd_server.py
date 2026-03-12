import socket

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))
print("UDP сервер запущен на порту 8080...")

while True:
    # Принимаем сообщение от клиента
    data, client_address = server_socket.recvfrom(1024)
    print(f"Получено от {client_address}: {data.decode()}")

    # Отправляем ответ
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
