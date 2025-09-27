#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 2: TCP Клиент для расчета площади параллелограмма
Клиент вводит параметры и получает площадь
"""

import socket

def main():
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Адрес сервера
    server_address = ('localhost', 12346)
    
    try:
        # Подключаемся к серверу
        client_socket.connect(server_address)
        print("Подключен к серверу")
        
        # Вводим параметры параллелограмма
        print("Введите параметры параллелограмма:")
        base = float(input("Основание: "))
        height = float(input("Высота: "))
        
        # Отправляем данные серверу
        data = f"{base},{height}"
        client_socket.send(data.encode('utf-8'))
        print(f"Отправлено серверу: {data}")
        
        # Получаем результат
        result = client_socket.recv(1024).decode('utf-8')
        print(f"Результат: {result}")
        
    except ValueError:
        print("Ошибка: введите корректные числовые значения")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
