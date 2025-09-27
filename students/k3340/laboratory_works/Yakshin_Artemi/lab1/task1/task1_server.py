#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 1: UDP Сервер
Сервер принимает сообщение "Hello, server" и отправляет "Hello, client"
"""

import socket

def main():
    # Создаем UDP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    
    print(f"UDP сервер запущен на {server_address}")
    print("Ожидание сообщений...")
    
    try:
        while True:
            # Получаем данные и адрес клиента
            data, client_address = server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            
            print(f"Получено от {client_address}: {message}")
            
            # Проверяем, что сообщение содержит "Hello, server"
            if "Hello, server" in message:
                response = "Hello, client"
                server_socket.sendto(response.encode('utf-8'), client_address)
                print(f"Отправлено клиенту {client_address}: {response}")
            else:
                error_msg = "Ошибка: ожидалось сообщение 'Hello, server'"
                server_socket.sendto(error_msg.encode('utf-8'), client_address)
                print(f"Отправлено клиенту {client_address}: {error_msg}")
                
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
