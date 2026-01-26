#!/usr/bin/env python3
"""
Задание 2: TCP клиент для математических операций
Отправляет параметры для вычисления по теореме Пифагора
"""

import socket

def main():
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Настройки сервера
    host = 'localhost'
    port = 9998
    
    try:
        # Подключаемся к серверу
        client_socket.connect((host, port))
        print(f"Подключено к серверу {host}:{port}")
        
        # Получаем входные данные от пользователя
        print("\nТеорема Пифагора: c = √(a² + b²)")
        a = input("Введите значение катета a: ")
        b = input("Введите значение катета b: ")
        
        # Отправляем данные серверу
        message = f"{a},{b}"
        client_socket.send(message.encode('utf-8'))
        print(f"Отправлено серверу: {message}")
        
        # Получаем результат от сервера
        response = client_socket.recv(1024).decode('utf-8')
        print(f"\nОтвет от сервера: {response}")
        
    except ConnectionRefusedError:
        print("Ошибка: не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрываем сокет
        client_socket.close()

if __name__ == "__main__":
    main()
