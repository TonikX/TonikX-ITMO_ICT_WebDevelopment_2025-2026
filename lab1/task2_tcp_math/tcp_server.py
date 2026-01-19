#!/usr/bin/env python3
"""
TCP Server для задания 2
Обрабатывает математические операции:
1. Теорема Пифагора
2. Решение квадратного уравнения
3. Поиск площади трапеции
4. Поиск площади параллелограмма
"""

import socket
import sys
import math

def pythagorean_theorem(a, b):
    """Вычисляет гипотенузу по теореме Пифагора"""
    try:
        a, b = float(a), float(b)
        if a <= 0 or b <= 0:
            return "Ошибка: катеты должны быть положительными числами"
        c = math.sqrt(a**2 + b**2)
        return f"Гипотенуза: {c:.2f}"
    except ValueError:
        return "Ошибка: введите корректные числа"

def quadratic_equation(a, b, c):
    """Решает квадратное уравнение ax² + bx + c = 0"""
    try:
        a, b, c = float(a), float(b), float(c)
        if a == 0:
            return "Ошибка: коэффициент 'a' не может быть равен 0"
        
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return f"Два корня: x1 = {x1:.2f}, x2 = {x2:.2f}"
        elif discriminant == 0:
            x = -b / (2*a)
            return f"Один корень: x = {x:.2f}"
        else:
            return "Нет действительных корней"
    except ValueError:
        return "Ошибка: введите корректные числа"

def trapezoid_area(a, b, h):
    """Вычисляет площадь трапеции"""
    try:
        a, b, h = float(a), float(b), float(h)
        if a <= 0 or b <= 0 or h <= 0:
            return "Ошибка: все параметры должны быть положительными числами"
        area = (a + b) * h / 2
        return f"Площадь трапеции: {area:.2f}"
    except ValueError:
        return "Ошибка: введите корректные числа"

def parallelogram_area(a, h):
    """Вычисляет площадь параллелограмма"""
    try:
        a, h = float(a), float(h)
        if a <= 0 or h <= 0:
            return "Ошибка: основание и высота должны быть положительными числами"
        area = a * h
        return f"Площадь параллелограмма: {area:.2f}"
    except ValueError:
        return "Ошибка: введите корректные числа"

def process_request(data):
    """Обрабатывает запрос от клиента"""
    try:
        parts = data.strip().split(',')
        operation = parts[0].strip()
        
        if operation == "1":  # Теорема Пифагора
            if len(parts) != 3:
                return "Ошибка: для теоремы Пифагора нужно 2 параметра (катеты)"
            return pythagorean_theorem(parts[1], parts[2])
        
        elif operation == "2":  # Квадратное уравнение
            if len(parts) != 4:
                return "Ошибка: для квадратного уравнения нужно 3 параметра (a, b, c)"
            return quadratic_equation(parts[1], parts[2], parts[3])
        
        elif operation == "3":  # Площадь трапеции
            if len(parts) != 4:
                return "Ошибка: для площади трапеции нужно 3 параметра (основание1, основание2, высота)"
            return trapezoid_area(parts[1], parts[2], parts[3])
        
        elif operation == "4":  # Площадь параллелограмма
            if len(parts) != 3:
                return "Ошибка: для площади параллелограмма нужно 2 параметра (основание, высота)"
            return parallelogram_area(parts[1], parts[2])
        
        else:
            return "Ошибка: неверный номер операции. Используйте 1, 2, 3 или 4"
    
    except Exception as e:
        return f"Ошибка обработки запроса: {str(e)}"

def main():
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Настройки сервера
    host = 'localhost'
    port = 12346
    
    try:
        # Привязываем сокет к адресу и порту
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"TCP Server запущен на {host}:{port}")
        print("Доступные операции:")
        print("1 - Теорема Пифагора (катет1, катет2)")
        print("2 - Квадратное уравнение (a, b, c)")
        print("3 - Площадь трапеции (основание1, основание2, высота)")
        print("4 - Площадь параллелограмма (основание, высота)")
        print("Ожидание подключений...")
        
        while True:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")
            
            try:
                # Получаем данные от клиента
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Получен запрос: {data}")
                
                # Обрабатываем запрос
                result = process_request(data)
                print(f"Результат: {result}")
                
                # Отправляем результат клиенту
                client_socket.send(result.encode('utf-8'))
                
            except Exception as e:
                error_msg = f"Ошибка обработки клиента: {str(e)}"
                print(error_msg)
                client_socket.send(error_msg.encode('utf-8'))
            
            finally:
                # Закрываем соединение с клиентом
                client_socket.close()
                print(f"Соединение с {client_address} закрыто")
    
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
        sys.exit(1)
    
    finally:
        # Закрываем серверный сокет
        server_socket.close()
        print("Сервер завершил работу")

if __name__ == "__main__":
    main()
