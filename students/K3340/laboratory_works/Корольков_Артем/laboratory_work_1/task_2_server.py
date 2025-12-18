import socket


def calculate_trapezoid_area(base_a, base_b, height):
    """Вычисляет площадь трапеции по формуле: S = (a + b) * h / 2"""
    try:
        a = float(base_a)
        b = float(base_b)
        h = float(height)
        area = (a + b) * h / 2
        return f"Площадь трапеции с основаниями {a} и {b} и высотой {h} равна: {area:.2f}"
    except ValueError:
        return "Ошибка: Все параметры должны быть числами!"


def main():
    # Создаем TCP-сокет (SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 12346)
    server_socket.bind(server_address)

    # Начинаем прослушивание входящих подключений
    server_socket.listen(1)
    print("Сервер запущен и ожидает подключений...")

    while True:
        try:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент: {client_address}")

            # Получаем данные от клиента
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Получены данные: {data}")

            # Разбираем параметры (ожидаем формат: a,b,h)
            params = data.split(',')
            if len(params) == 3:
                result = calculate_trapezoid_area(params[0], params[1], params[2])
            else:
                result = "Ошибка: Неверный формат данных. Ожидается: основание1,основание2,высота"

            # Отправляем результат клиенту
            client_socket.sendall(result.encode('utf-8'))
            print(f"Отправлен результат: {result}")

            # Закрываем соединение с клиентом
            client_socket.close()

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            if 'client_socket' in locals():
                client_socket.close()


if __name__ == "__main__":
    main()