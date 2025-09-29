import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 50001

def run_client():
    # Создаем UDP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Адрес сервера
    server_address = (SERVER_HOST, SERVER_PORT)
    
    print("Отправка сообщения на сервер...")

    # Отправляем сообщение серверу
    message = "Hello, server"
    client_socket.sendto(message.encode(), server_address)
    
    # Получаем ответ от сервера
    data, _ = client_socket.recvfrom(1024)  # Буфер размером 1024 байта
    print(f"Получено сообщение от сервера: {data.decode()}")
    
    # Закрываем сокет
    client_socket.close()

if __name__ == "__main__":
    run_client()
