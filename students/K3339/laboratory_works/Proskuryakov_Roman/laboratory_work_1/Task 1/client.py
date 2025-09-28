import socket

def start_client():
    # Создаем UDP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Адрес сервера
    server_address = ('localhost', 12345)
    
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
    start_client()
