import socket
import math
import json

# параметры сервера
HOST = 'localhost'
PORT = 8081

# создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# начинаем слушать входящие соединения
server_socket.listen(5)
print(f"TCP сервер запущен на {HOST}:{PORT}...")
print("Ожидание подключений клиентов...")

def pythagorean_theorem(a, b):
    """теорема Пифагора: c = sqrt(a² + b²)"""
    c = math.sqrt(a**2 + b**2)
    return f"Гипотенуза c = {c:.4f}"

def quadratic_equation(a, b, c):
    """решение квадратного уравнения: ax² + bx + c = 0"""
    if a == 0:
        return "Ошибка: коэффициент 'a' не может быть равен 0"
    
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return f"x₁ = {x1:.4f}, x₂ = {x2:.4f}"
    elif discriminant == 0:
        x = -b / (2*a)
        return f"x = {x:.4f} (один корень)"
    else:
        return "Уравнение не имеет действительных корней"

def trapezoid_area(a, b, h):
    """площадь трапеции: S = (a + b) * h / 2"""
    area = (a + b) * h / 2
    return f"Площадь трапеции S = {area:.4f}"

def parallelogram_area(a, h):
    """площадь параллелограмма: S = a * h"""
    area = a * h
    return f"Площадь параллелограмма S = {area:.4f}"

def process_request(data):
    """обработка запроса от клиента"""
    try:
        request = json.loads(data)
        operation = request.get('operation')
        params = request.get('params', [])
        
        if operation == 1:  # Теорема Пифагора
            if len(params) == 2:
                a, b = params
                return pythagorean_theorem(a, b)
            else:
                return "Ошибка: для теоремы Пифагора нужно 2 параметра (катеты)"
                
        elif operation == 2:  # Квадратное уравнение
            if len(params) == 3:
                a, b, c = params
                return quadratic_equation(a, b, c)
            else:
                return "Ошибка: для квадратного уравнения нужно 3 параметра (a, b, c)"
                
        elif operation == 3:  # Площадь трапеции
            if len(params) == 3:
                a, b, h = params
                return trapezoid_area(a, b, h)
            else:
                return "Ошибка: для площади трапеции нужно 3 параметра (основания a, b и высота h)"
                
        elif operation == 4:  # Площадь параллелограмма
            if len(params) == 2:
                a, h = params
                return parallelogram_area(a, h)
            else:
                return "Ошибка: для площади параллелограмма нужно 2 параметра (сторона и высота)"
                
        else:
            return "Ошибка: неизвестная операция. Доступные операции: 1-4"
            
    except json.JSONDecodeError:
        return "Ошибка: неверный формат данных"
    except Exception as e:
        return f"Ошибка: {str(e)}"

while True:
    try:
        # принимаем соединение от клиента
        client_connection, client_address = server_socket.accept()
        print(f'Подключение от {client_address}')
        
        # получаем данные от клиента
        data = client_connection.recv(1024).decode('utf-8')
        print(f'Получен запрос: {data}')
        
        # обрабатываем запрос
        result = process_request(data)
        print(f'Результат: {result}')
        
        # отправляем результат клиенту
        response = json.dumps({'result': result, 'status': 'success'})
        client_connection.sendall(response.encode('utf-8'))
        
        # закрываем соединение
        client_connection.close()
        
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
        break
    except Exception as e:
        print(f"Ошибка: {e}")

# закрываем сокет
server_socket.close()
print("Сервер завершил работу")

