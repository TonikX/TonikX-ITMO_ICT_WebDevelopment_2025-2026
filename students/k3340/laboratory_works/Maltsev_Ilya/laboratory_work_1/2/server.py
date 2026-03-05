import math
import socket


def calculate_quadratic_equation(a, b, c):
    if a == 0:
        if b == 0:
            return "Нет решений" if c != 0 else "Бесконечно много решений"
        return f"Линейное уравнение, корень: {-c / b}"

    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"Два корня: {x1:.4f}, {x2:.4f}"
    elif discriminant == 0:
        x = -b / (2 * a)
        return f"Один корень: {x:.4f}"
    else:
        return "Нет вещественных корней"


def handle_client(client_connection, client_address):
    try:
        print(f'Подключение от {client_address}')
        data = client_connection.recv(1024).decode()
        if not data:
            return
        try:
            a, b, c = map(int, data.split())
            result = calculate_quadratic_equation(a, b, c)
        except ValueError:
            result = "Ошибка: Ожидались три целых числа"

        client_connection.send(str(result).encode())
        print(f'Отправлен результат: {result}')
    except ConnectionResetError:
        print(f"Ошибка: соединение с {client_address} разорвано.")
    finally:
        client_connection.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)

    print("Сервер запущен на порту 8080...")

    try:
        while True:
            client_connection, client_address = server_socket.accept()
            handle_client(client_connection, client_address)
    except KeyboardInterrupt:
        print("\nВыключение сервера...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
