#!/usr/bin/env python3
"""
Задание 2: TCP сервер для математических операций
Вариант: Теорема Пифагора (c = √(a² + b²))
"""

import socket
import math

def calculate_pythagorean(a, b):
    """Вычисляет гипотенузу по теореме Пифагора"""
    c = math.sqrt(a**2 + b**2)
    return c

def main():
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Настройки сервера
    host = 'localhost'
    port = 9998
    
    # Привязываем сокет к адресу и порту
    server_socket.bind((host, port))
    
    # Начинаем прослушивание (максимум 5 соединений в очереди)
    server_socket.listen(5)
    
    print(f"TCP сервер запущен на {host}:{port}")
    print("Ожидание подключений клиентов...\n")
    
    while True:
        # Принимаем подключение
        client_socket, client_address = server_socket.accept()
        print(f"Подключен клиент: {client_address}")
        
        try:
            # Получаем данные от клиента
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Получено: {data}")
            
            # Парсим данные (ожидаем формат: "a,b")
            a, b = map(float, data.split(','))
            
            # Вычисляем результат
            c = calculate_pythagorean(a, b)
            
            # Формируем ответ
            response = f"Теорема Пифагора: a={a}, b={b}, c={c:.4f}"
            print(f"Результат: {response}")
            
            # Отправляем результат клиенту
            client_socket.send(response.encode('utf-8'))
            
        except ValueError:
            error_msg = "Ошибка: неверный формат данных. Ожидается: a,b"
            client_socket.send(error_msg.encode('utf-8'))
            print(error_msg)
        except Exception as e:
            error_msg = f"Ошибка: {str(e)}"
            client_socket.send(error_msg.encode('utf-8'))
            print(error_msg)
        finally:
            # Закрываем соединение с клиентом
            client_socket.close()
            print(f"Соединение с {client_address} закрыто\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
