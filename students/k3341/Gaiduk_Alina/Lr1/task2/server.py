import socket
import math

def run_server():
    # Создаем TCP-сокет, (AF_INET - IPv4, SOCK_STREAM - TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 11111))
        # Переводим сокет в режим ожидания входящих соединений
        server_socket.listen()
        print("Сервер запущен на порту 11111...")
        while True:
            # ожидаем новый сокет и адрес клиента
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Подключился клиент с адресом {client_address}")
                client_message = client_socket.recv(1024).decode("UTF-8")
                try:
                    a, b = client_message.strip().split()
                    a, b = float(a), float(b)
                    c = math.hypot(a, b)
                    result = f"Гипотенуза равна {c:.4f}"
                # Ловим любые ошибки
                except Exception as e:
                    result = f"Ошибка: {e}"
                # Отправляем ответ или ошибку
                client_socket.sendall(result.encode("UTF-8"))

if __name__ == "__main__":
    run_server()


