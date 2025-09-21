#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 2: TCP Математические операции
Клиент запрашивает выполнение математической операции,
сервер обрабатывает данные и возвращает результат

Варианты операций:
1. Теорема Пифагора
2. Решение квадратного уравнения  
3. Площадь трапеции
4. Площадь параллелограмма
"""

import socket
import sys
import json
import math
import threading
import time

def pythagorean_theorem(a, b):
    """Теорема Пифагора: c = √(a² + b²)"""
    return math.sqrt(a**2 + b**2)

def quadratic_equation(a, b, c):
    """Решение квадратного уравнения: ax² + bx + c = 0"""
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return f"Корни: x1={x1:.2f}, x2={x2:.2f}"
    else:
        return "Нет действительных корней"

def trapezoid_area(a, b, h):
    """Площадь трапеции: S = (a + b) × h / 2"""
    return (a + b) * h / 2

def parallelogram_area(a, h):
    """Площадь параллелограмма: S = a × h"""
    return a * h

def tcp_math_server():
    """TCP сервер для математических операций"""
    print("=== TCP Математический Сервер ===")
    
    # Создание TCP сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('localhost', 12346))
        server_socket.listen(1)
        print("TCP математический сервер запущен на порту 12346")
        print("Ожидание подключений...")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Подключен клиент: {addr}")
            
            try:
                # Получение запроса от клиента
                data = client_socket.recv(1024)
                request = json.loads(data.decode('utf-8'))
                
                operation = request['operation']
                params = request['params']
                
                # Обработка различных операций
                if operation == 1:  # Теорема Пифагора
                    a, b = params['a'], params['b']
                    result = pythagorean_theorem(a, b)
                    response = f"Гипотенуза: {result:.2f}"
                    
                elif operation == 2:  # Квадратное уравнение
                    a, b, c = params['a'], params['b'], params['c']
                    response = quadratic_equation(a, b, c)
                    
                elif operation == 3:  # Площадь трапеции
                    a, b, h = params['a'], params['b'], params['h']
                    result = trapezoid_area(a, b, h)
                    response = f"Площадь трапеции: {result:.2f}"
                    
                elif operation == 4:  # Площадь параллелограмма
                    a, h = params['a'], params['h']
                    result = parallelogram_area(a, h)
                    response = f"Площадь параллелограмма: {result:.2f}"
                else:
                    response = "Неизвестная операция"
                
                # Отправка результата клиенту
                client_socket.send(response.encode('utf-8'))
                print(f"Отправлен результат: {response}")
                
            except Exception as e:
                error_response = f"Ошибка: {str(e)}"
                client_socket.send(error_response.encode('utf-8'))
                print(f"Ошибка обработки: {e}")
            finally:
                client_socket.close()
                
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        server_socket.close()

def tcp_math_client():
    """TCP клиент для математических операций"""
    print("=== TCP Математический Клиент ===")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(('localhost', 12346))
        
        # Выбор операции
        print("\nВыберите операцию:")
        print("1. Теорема Пифагора")
        print("2. Квадратное уравнение")
        print("3. Площадь трапеции")
        print("4. Площадь параллелограмма")
        
        operation = int(input("Введите номер операции: "))
        
        # Ввод параметров в зависимости от операции
        if operation == 1:  # Теорема Пифагора
            a = float(input("Введите катет a: "))
            b = float(input("Введите катет b: "))
            params = {'a': a, 'b': b}
            
        elif operation == 2:  # Квадратное уравнение
            a = float(input("Введите коэффициент a: "))
            b = float(input("Введите коэффициент b: "))
            c = float(input("Введите коэффициент c: "))
            params = {'a': a, 'b': b, 'c': c}
            
        elif operation == 3:  # Площадь трапеции
            a = float(input("Введите основание a: "))
            b = float(input("Введите основание b: "))
            h = float(input("Введите высоту h: "))
            params = {'a': a, 'b': b, 'h': h}
            
        elif operation == 4:  # Площадь параллелограмма
            a = float(input("Введите основание a: "))
            h = float(input("Введите высоту h: "))
            params = {'a': a, 'h': h}
        else:
            print("Неверная операция!")
            return
        
        # Формирование запроса
        request = {
            'operation': operation,
            'params': params
        }
        
        # Отправка запроса
        client_socket.send(json.dumps(request).encode('utf-8'))
        
        # Получение ответа
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Результат: {response}")
        
    except Exception as e:
        print(f"Ошибка клиента: {e}")
    finally:
        client_socket.close()

def run_demo():
    """Демонстрация работы TCP математического сервера"""
    print("=== Демонстрация TCP Математика ===")
    
    # Запуск сервера в отдельном потоке
    server_thread = threading.Thread(target=tcp_math_server, daemon=True)
    server_thread.start()
    
    # Небольшая задержка для запуска сервера
    time.sleep(1)
    
    # Демонстрационные вычисления
    demos = [
        (1, {'a': 3, 'b': 4}),  # Теорема Пифагора
        (2, {'a': 1, 'b': -5, 'c': 6}),  # Квадратное уравнение
        (3, {'a': 5, 'b': 7, 'h': 4}),  # Площадь трапеции
        (4, {'a': 6, 'h': 8})  # Площадь параллелограмма
    ]
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(('localhost', 12346))
        
        for operation, params in demos:
            request = {'operation': operation, 'params': params}
            client_socket.send(json.dumps(request).encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Операция {operation}: {response}")
            time.sleep(0.5)
            
    except Exception as e:
        print(f"Ошибка демо: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            tcp_math_server()
        elif sys.argv[1] == "client":
            tcp_math_client()
        elif sys.argv[1] == "demo":
            run_demo()
        else:
            print("Использование: python task2_tcp_math.py [server|client|demo]")
    else:
        print("Использование:")
        print("  python task2_tcp_math.py server  - запустить сервер")
        print("  python task2_tcp_math.py client  - запустить клиент")
        print("  python task2_tcp_math.py demo    - демонстрация")
