import socket

from routes import main_router

# AF_INET - IPv4, SOCK_STREAM - TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Решение проблемы Address already in use. Игнорирование состояния сокета TIME_WAIT
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp_socket.bind(('localhost', 9999))
tcp_socket.listen(5)

print("Учет котиков запущен на http://localhost:9999")

while True:
    client_socket, addr = tcp_socket.accept()
    print(f"Новое подключение от {str(addr)}")

    request = client_socket.recv(1024).decode('utf-8')
    if not request:
        continue
    response = main_router(request)
    client_socket.sendall(response)
    client_socket.close()
