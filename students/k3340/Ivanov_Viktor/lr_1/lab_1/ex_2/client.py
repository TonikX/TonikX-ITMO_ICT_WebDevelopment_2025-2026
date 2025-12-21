import socket
import json

# параметры сервера
HOST = 'localhost'
PORT = 8081

def get_operation_choice():
    """получение выбора операции от пользователя"""
    print("\n=== Доступные математические операции ===")
    print("1. Теорема Пифагора (c = √(a² + b²))")
    print("2. Решение квадратного уравнения (ax² + bx + c = 0)")
    print("3. Площадь трапеции (S = (a + b) * h / 2)")
    print("4. Площадь параллелограмма (S = a * h)")
    print("0. Выход")
    
    while True:
        try:
            choice = int(input("\nВыберите операцию (0-4): "))
            if 0 <= choice <= 4:
                return choice
            else:
                print("Ошибка: выберите число от 0 до 4")
        except ValueError:
            print("Ошибка: введите целое число")

def get_pythagorean_params():
    """получение параметров для теоремы Пифагора"""
    print("\n=== Теорема Пифагора ===")
    print("Введите длины катетов:")
    a = float(input("Катет a: "))
    b = float(input("Катет b: "))
    return [a, b]

def get_quadratic_params():
    """получение параметров для квадратного уравнения"""
    print("\n=== Квадратное уравнение ax² + bx + c = 0 ===")
    a = float(input("Коэффициент a: "))
    b = float(input("Коэффициент b: "))
    c = float(input("Коэффициент c: "))
    return [a, b, c]

def get_trapezoid_params():
    """получение параметров для площади трапеции"""
    print("\n=== Площадь трапеции ===")
    a = float(input("Основание a: "))
    b = float(input("Основание b: "))
    h = float(input("Высота h: "))
    return [a, b, h]

def get_parallelogram_params():
    """получение параметров для площади параллелограмма"""
    print("\n=== Площадь параллелограмма ===")
    a = float(input("Сторона a: "))
    h = float(input("Высота h: "))
    return [a, h]

def send_request(operation, params):
    """отправка запроса на сервер"""
    try:
        # создаем TCP сокет
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # подключаемся к серверу
        client_socket.connect((HOST, PORT))
        
        # формируем запрос
        request = {
            'operation': operation,
            'params': params
        }
        
        # отправляем запрос серверу
        client_socket.sendall(json.dumps(request).encode('utf-8'))
        
        # получаем ответ от сервера
        response = client_socket.recv(1024).decode('utf-8')
        
        # закрываем соединение
        client_socket.close()
        
        # парсим ответ
        result = json.loads(response)
        return result.get('result', 'Ошибка: неверный ответ сервера')
        
    except ConnectionRefusedError:
        return "Ошибка: не удалось подключиться к серверу"
    except Exception as e:
        return f"Ошибка: {str(e)}"

def main():
    """основная функция клиента"""
    print("=== Математический TCP клиент ===")
    print("Подключение к серверу:", f"{HOST}:{PORT}")
    
    while True:
        operation = get_operation_choice()
        
        if operation == 0:
            print("До свидания!")
            break
        
        # получаем параметры в зависимости от выбранной операции
        if operation == 1:
            params = get_pythagorean_params()
        elif operation == 2:
            params = get_quadratic_params()
        elif operation == 3:
            params = get_trapezoid_params()
        elif operation == 4:
            params = get_parallelogram_params()
        else:
            print("Неизвестная операция")
            continue
        
        # отправляем запрос на сервер
        print("\nОтправка запроса на сервер...")
        result = send_request(operation, params)
        
        # выводим результат
        print(f"\nРезультат: {result}")
        
        # спрашиваем, хочет ли пользователь продолжить
        continue_choice = input("\nПродолжить? (y/n): ").lower()
        if continue_choice not in ['y', 'yes', 'да', 'д']:
            print("До свидания!")
            break

if __name__ == "__main__":
    main()

