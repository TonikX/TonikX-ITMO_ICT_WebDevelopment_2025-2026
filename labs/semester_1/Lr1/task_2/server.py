import socket

def calculate_trapezoid_area(a, b, h):
    """
    Функция для нахождения площади трапеции.
    """
    return ((a + b) / 2) * h

def main():
    # Создаём сокет сервера для TCP-соединений
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Запускаем сервер на localhost
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)

    # Устанавливаем максимальный размер очереди подключений
    server_socket.listen(5)

    print(f"TCP-сервер запущен на {server_address}. Ожидание подключений...")

    # Цикл работы сервера с отловом ошибок
    try:
        while True:
            # При подключении создаём сокет клиента
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент: {client_address}")

            # Декодируем запрос клиента
            data = client_socket.recv(1024).decode()
            print(f"Получено от {client_address}: {data}")

            # Рассчитываем площадь трапеции и подготавливаем ответ
            try:
                a, b, h = map(float, data.split(','))
                response = ""
                if (a <= 0) or (b <= 0) or (h <= 0):
                    response = "Ошибка: a,b,h должны быть положительными числами"
                else:
                    area = calculate_trapezoid_area(a, b, h)
                    response = f"Площадь трапеции: {area:.2f}"

            # В случае ошибки передаём её в качестве ответа
            except Exception as e:
                response = f"Ошибка при вычислении: {str(e)}"
            
            # Отправляем ответ
            client_socket.send(response.encode())
            print(f"Отправлен ответ: {response}")
            
            # Закрываем клиентский сокет
            client_socket.close()

    # Отлавливаем ошибки
    except Exception as e:
        print(f"\nВозникла ошибка: {str(e)}")
    finally:
        # При завершении работы закрываем сокет сервера
        server_socket.close()

if __name__ == "__main__":
    main()
