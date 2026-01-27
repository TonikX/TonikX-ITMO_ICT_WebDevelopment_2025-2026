import json
import math
import socket


# Параметры сервера
HOST = '127.0.0.1'
PORT = 8089


def solve_quadratic(a, b, c):
    """Решает квадратное уравнение ax^2 + bx + c = 0 и возвращает результат в словаре."""

    # Инициализация словаря для результата
    result = {"equation": f"{a}x^2 + {b}x + {c} = 0", "status": "success", "roots": []}

    if a == 0:
        if b == 0:
            result["status"] = "error"
            result["message"] = "Не квадратное уравнение: a и b равны 0."
        else:
            # Линейное уравнение bx + c = 0
            x = -c / b
            result["message"] = "Линейное уравнение"
            result["roots"] = [{"x": round(x, 4)}]
        return result

    # Вычисляем дискриминант
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        # Корни комплексные
        real_part = -b / (2 * a)
        imaginary_part = math.sqrt(abs(discriminant)) / (2 * a)
        result["message"] = "Комплексные корни"
        result["roots"] = [
            {"x1": f"{round(real_part, 4)} + {round(imaginary_part, 4)}i"},
            {"x2": f"{round(real_part, 4)} - {round(imaginary_part, 4)}i"}
        ]
    elif discriminant == 0:
        # Один действительный корень
        x = -b / (2 * a)
        result["message"] = "Один действительный корень"
        result["roots"] = [{"x": round(x, 4)}]
    else:
        # Два действительных корня
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        result["message"] = "Два действительных корня"
        result["roots"] = [{"x1": round(x1, 4)}, {"x2": round(x2, 4)}]

    return result


def start_server():
    """Запускает TCP-сервер, обрабатывающий JSON."""
    print(f"Сервер запускается на {HOST}:{PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Сервер запущен. Ожидание соединения...")

        # Основной цикл для обработки одного клиента
        connection, address = s.accept()
        with connection:
            print(f"Соединение установлено с {address}")
            data = connection.recv(1024)

            if not data:
                return

            received_json_str = data.decode('utf-8')
            print(f"Получены данные (JSON) от клиента: {received_json_str}")

            response_data = {}
            try:
                # 1. Декодирование JSON
                coeffs = json.loads(received_json_str)

                # Проверка наличия всех коэффициентов
                a = coeffs['a']
                b = coeffs['b']
                c = coeffs['c']

                # 2. Решение уравнения
                response_data = solve_quadratic(a, b, c)

            except json.JSONDecodeError:
                response_data = {"status": "error", "message": "Ошибка декодирования JSON. Неверный формат."}
            except KeyError:
                response_data = {"status": "error", "message": "Ошибка: Отсутствует один из ключей (a, b, c)."}
            except Exception as e:
                response_data = {"status": "error", "message": f"Неизвестная ошибка на сервере: {e}"}

            # 3. Отправка ответа (JSON)
            response_json_str = json.dumps(response_data)
            print(f"Отправка ответа: {response_data['status']}")
            connection.sendall(response_json_str.encode('utf-8'))




if __name__ == '__main__':
    start_server()
