import socket

def handle_client(client_socket):
    # Получаем запрос от клиента
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Request received:\n{request}")

    # Читаем содержимое файла index.html
    with open(r"C:\Users\Lenovo\Desktop\ITMO_2025\Web_Programming\First_lab\Thrid_task\index.html", 'r') as file:
        content = file.read()

    # Формируем HTTP-ответ с HTML-контентом
    response = f"""HTTP/1.1 200 OK
Content-Type: text/html

{content}"""

    # Отправляем ответ клиенту
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def start_server():
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Привязываем сокет к адресу и порту (localhost:8080)
    server_socket.bind(('localhost', 8080))
    # Переводим сервер в режим ожидания соединений (до 1 клиента в очереди)
    server_socket.listen(1)
    print("Server is listening on port 8080...")

    while True:
        # Принимаем входящее соединение от клиента
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        # Передаём клиента в обработчик
        handle_client(client_socket)

# Запуск сервера
start_server()
