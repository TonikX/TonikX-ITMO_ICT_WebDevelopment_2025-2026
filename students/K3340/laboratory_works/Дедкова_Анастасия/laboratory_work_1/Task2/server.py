import socket
import math

HOST = 'localhost'
PORT = 9091


def handle_client(conn, addr):
    """Обработка подключения клиента."""
    print(f"Подключение от {addr}")
    try:
        # Получаем данные от клиента
        data = conn.recv(1024).decode('utf-8')
        print(f"Получено от клиента: {data}")

        # Ожидаем, что клиент отправит два числа
        parts = data.strip().split()
        if len(parts) != 2:
            response = "Ошибка: введите два числа (катеты a и b)"
        else:
            a, b = map(float, parts)
            c = math.sqrt(a ** 2 + b ** 2)
            response = f"Гипотенуза: {c:.2f}"

        # Отправляем результат клиенту
        conn.sendall(response.encode('utf-8'))
        print(f"Отправлено клиенту: {response}")

    except Exception as e:
        print(f"Ошибка при обработке клиента {addr}: {e}")
    finally:
        conn.close()
        print(f"Соединение с {addr} закрыто")


def start_server():
    """Запуск TCP-сервера для вычисления гипотенузы."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"TCP сервер запущен на {HOST}:{PORT}, ожидаем подключения...")

    try:
        while True:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
