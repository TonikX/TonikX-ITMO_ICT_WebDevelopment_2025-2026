import socket

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Сервер запущен и ожидает сообщений...")

while True:
    # Получаем данные и адрес клиента
    data, client_address = server_socket.recvfrom(1024)
    print(f"Получено сообщение от {client_address}: {data.decode('utf-8')}")

    # Формируем ответ
    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), client_address)
    print(f"Отправлен ответ: {response}")