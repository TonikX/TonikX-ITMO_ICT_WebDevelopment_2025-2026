import socket
import math


def handle_pythagoras(data):
    """Обработка теоремы Пифагора"""
    try:
        # Разбираем данные: катет1, катет2
        parts = data.split(',')
        if len(parts) != 2:
            return "Ошибка: необходимо ввести два катета через запятую"

        a = float(parts[0])
        b = float(parts[1])

        if a <= 0 or b <= 0:
            return "Ошибка: катеты должны быть положительными числами"

        # Вычисляем гипотенузу
        c = math.sqrt(a ** 2 + b ** 2)

        return f"Гипотенуза треугольника с катетами {a} и {b} = {c:.2f}"

    except ValueError:
        return "Ошибка: введите числа в правильном формате"
    except Exception as e:
        return f"Ошибка при вычислении: {e}"


def start_server():
    """Запуск TCP сервера"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(('localhost', 8080))
        server_socket.listen(5)
        print("Сервер запущен на localhost:8080")
        print("Ожидание подключений...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")

            try:
                # Получаем данные от клиента
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Получены данные: {data}")

                # Обрабатываем запрос
                result = handle_pythagoras(data)

                # Отправляем результат клиенту
                client_socket.send(result.encode('utf-8'))
                print(f"Отправлен результат: {result}")

            except Exception as e:
                error_msg = f"Ошибка обработки запроса: {e}"
                client_socket.send(error_msg.encode('utf-8'))
            finally:
                client_socket.close()
                print(f"Соединение с {client_address} закрыто\n")

    except KeyboardInterrupt:
        print("\nСервер остановлен")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()