import socket

HOST = "127.0.0.1"
PORT = 50001

def run_server():
    # Создаем UDP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Привязываем сокет к адресу и порту
    server_address = (HOST, PORT)
    server_socket.bind(server_address)
    
    print("Сервер запущен и ожидает сообщений...")
    
    while True:
        # Получаем данные от клиента
        data, client_address = server_socket.recvfrom(1024)  # Буфер размером 1024 байта
        print(f"Получено сообщение от клиента: {data.decode()}")
        
        # Отправляем ответ клиенту
        response_message = "Hello, client"
        server_socket.sendto(response_message.encode(), client_address)

if __name__ == "__main__":
    run_server()
