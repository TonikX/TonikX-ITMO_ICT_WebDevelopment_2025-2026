import json
import socket

# Параметры сервера для подключения
HOST = '127.0.0.1'
PORT = 8089


def start_client():
    """Запускает TCP-клиент, отправляющий JSON."""
    print("Введите коэффициенты квадратного уравнения (ax^2 + bx + c = 0).")
    try:
        a = float(input("Введите коэффициент 'a': "))
        b = float(input("Введите коэффициент 'b': "))
        c = float(input("Введите коэффициент 'c': "))
    except ValueError:
        print("Ошибка ввода: Введите числовые значения.")
        return

    # 1. Формирование Python-словаря
    data_dict = {
        "a": a,
        "b": b,
        "c": c
    }

    # 2. Кодирование словаря в JSON-строку
    data_to_send = json.dumps(data_dict)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print(f"Подключение к серверу {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            print("Соединение установлено.")

            # 3. Отправка JSON-строки
            print(f"Отправка данных (JSON): {data_to_send}")
            s.sendall(data_to_send.encode('utf-8'))

            # 4. Получение ответа от сервера
            print("Ожидание ответа от сервера...")
            data = s.recv(1024)

            received_json_str = data.decode('utf-8')

            # 5. Декодирование ответа
            result = json.loads(received_json_str)

            # Вывод результата
            print("\n--- Результат от сервера ---")

            if result.get("status") == "success":
                print(f"Уравнение: {result['equation']}")
                print(f"Статус: {result['message']}")
                print("Корни:")
                for root in result['roots']:
                    print(f"  {root}")
            else:
                print(f"Ошибка: {result.get('message', 'Неизвестная ошибка')}")

            print("----------------------------\n")

        except ConnectionRefusedError:
            print(f"Ошибка: Не удалось подключиться к серверу {HOST}:{PORT}. Убедитесь, что сервер запущен.")
        except json.JSONDecodeError:
            print("Ошибка: Получен неверный JSON-ответ от сервера.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    start_client()
