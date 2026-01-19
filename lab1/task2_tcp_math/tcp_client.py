#!/usr/bin/env python3
"""
TCP Client для задания 2
Интерактивный клиент для выполнения математических операций
"""

import socket
import sys

def get_operation_choice():
    """Получает выбор операции от пользователя"""
    print("\nДоступные математические операции:")
    print("1 - Теорема Пифагора")
    print("2 - Решение квадратного уравнения")
    print("3 - Поиск площади трапеции")
    print("4 - Поиск площади параллелограмма")
    print("0 - Выход")
    
    while True:
        try:
            choice = input("\nВыберите операцию (0-4): ").strip()
            if choice in ['0', '1', '2', '3', '4']:
                return choice
            else:
                print("Ошибка: введите число от 0 до 4")
        except KeyboardInterrupt:
            print("\nВыход...")
            return '0'

def get_pythagorean_params():
    """Получает параметры для теоремы Пифагора"""
    print("\nТеорема Пифагора: c = √(a² + b²)")
    try:
        a = float(input("Введите длину первого катета: "))
        b = float(input("Введите длину второго катета: "))
        return f"1,{a},{b}"
    except ValueError:
        print("Ошибка: введите корректные числа")
        return None

def get_quadratic_params():
    """Получает параметры для квадратного уравнения"""
    print("\nКвадратное уравнение: ax² + bx + c = 0")
    try:
        a = float(input("Введите коэффициент a: "))
        b = float(input("Введите коэффициент b: "))
        c = float(input("Введите коэффициент c: "))
        return f"2,{a},{b},{c}"
    except ValueError:
        print("Ошибка: введите корректные числа")
        return None

def get_trapezoid_params():
    """Получает параметры для площади трапеции"""
    print("\nПлощадь трапеции: S = (a + b) * h / 2")
    try:
        a = float(input("Введите длину первого основания: "))
        b = float(input("Введите длину второго основания: "))
        h = float(input("Введите высоту: "))
        return f"3,{a},{b},{h}"
    except ValueError:
        print("Ошибка: введите корректные числа")
        return None

def get_parallelogram_params():
    """Получает параметры для площади параллелограмма"""
    print("\nПлощадь параллелограмма: S = a * h")
    try:
        a = float(input("Введите длину основания: "))
        h = float(input("Введите высоту: "))
        return f"4,{a},{h}"
    except ValueError:
        print("Ошибка: введите корректные числа")
        return None

def send_request(server_host, server_port, request):
    """Отправляет запрос серверу и получает ответ"""
    try:
        # Создаем TCP сокет
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Подключаемся к серверу
        client_socket.connect((server_host, server_port))
        
        # Отправляем запрос
        client_socket.send(request.encode('utf-8'))
        print(f"Отправлен запрос: {request}")
        
        # Получаем ответ
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Результат: {response}")
        
        return response
        
    except ConnectionRefusedError:
        print("Ошибка: не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
        return None
    except Exception as e:
        print(f"Ошибка соединения: {e}")
        return None
    finally:
        client_socket.close()

def main():
    # Настройки сервера
    server_host = 'localhost'
    server_port = 12346
    
    print("TCP Math Client")
    print("===============")
    
    while True:
        choice = get_operation_choice()
        
        if choice == '0':
            print("До свидания!")
            break
        
        # Получаем параметры в зависимости от выбранной операции
        request = None
        if choice == '1':
            request = get_pythagorean_params()
        elif choice == '2':
            request = get_quadratic_params()
        elif choice == '3':
            request = get_trapezoid_params()
        elif choice == '4':
            request = get_parallelogram_params()
        
        if request is None:
            print("Попробуйте еще раз с корректными данными.")
            continue
        
        # Отправляем запрос серверу
        send_request(server_host, server_port, request)
        
        # Спрашиваем, хочет ли пользователь продолжить
        try:
            continue_choice = input("\nХотите выполнить еще одну операцию? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', 'да', 'д']:
                print("До свидания!")
                break
        except KeyboardInterrupt:
            print("\nДо свидания!")
            break

if __name__ == "__main__":
    main()
