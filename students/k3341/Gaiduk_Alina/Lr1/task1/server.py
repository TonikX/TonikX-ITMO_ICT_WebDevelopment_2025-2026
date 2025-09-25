import socket

def run_server():
    # Создаем UDP-сокет, (AF_INET - IPv4, SOCK_DGRAM - UDP)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(('127.0.0.1', 11111))
        print("Сервер запущен на порту 11111...")
        while True:
            # Ждем датаграмму до 1024 байт
            data, client_address = server_socket.recvfrom(1024)
            # Преобразуем байты в строку
            client_message = data.decode("UTF-8")
            print(f"Получено сообщение от клиента {client_address}: {client_message}")
            if client_message == "Hello, server":
                server_message = "Hello, client"
                # Перед отправкой клиенту кодируем строку в байты
                server_socket.sendto(server_message.encode("UTF-8"), client_address)


if __name__ == "__main__":
    run_server()




