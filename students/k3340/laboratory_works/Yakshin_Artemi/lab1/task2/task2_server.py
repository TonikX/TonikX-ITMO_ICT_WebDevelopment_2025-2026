#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 2: TCP Сервер для расчета площади параллелограмма
Сервер принимает параметры параллелограмма и возвращает площадь
"""

import socket
import math

def calculate_parallelogram_area(base, height):
    """Вычисляет площадь параллелограмма"""
    return base * height

def main():
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 12346)
    server_socket.bind(server_address)
    server_socket.listen(5)
    
    print(f"TCP сервер запущен на {server_address}")
    print("Ожидание подключений...")
    
    try:
        while True:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")
            
            try:
                # Получаем данные от клиента
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Получено от клиента: {data}")
                
                # Парсим данные (ожидаем формат: "base,height")
                try:
                    base, height = map(float, data.split(','))
                    
                    # Вычисляем площадь
                    area = calculate_parallelogram_area(base, height)
                    
                    # Отправляем результат
                    result = f"Площадь параллелограмма: {area:.2f}"
                    client_socket.send(result.encode('utf-8'))
                    print(f"Отправлено клиенту: {result}")
                    
                except ValueError:
                    error_msg = "Ошибка: неверный формат данных. Ожидается: base,height"
                    client_socket.send(error_msg.encode('utf-8'))
                    print(f"Отправлено клиенту: {error_msg}")
                    
            except Exception as e:
                print(f"Ошибка при обработке клиента: {e}")
            finally:
                client_socket.close()
                print(f"Соединение с {client_address} закрыто")
                
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
