#!/usr/bin/env python3
"""
UDP Server для задания 1
Принимает сообщение "Hello, server" от клиента и отправляет ответ "Hello, client"
"""

import socket
import sys

def main():
    # Создаем UDP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Настройки сервера
    host = 'localhost'
    port = 12345
    
    try:
        # Привязываем сокет к адресу и порту
        server_socket.bind((host, port))
        print(f"UDP Server запущен на {host}:{port}")
        print("Ожидание сообщений от клиента...")
        
        # Получаем сообщение от клиента
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')
        
        print(f"Получено сообщение от {client_address}: {message}")
        
        # Отправляем ответ клиенту
        response = "Hello, client"
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Отправлен ответ клиенту: {response}")
        
    except Exception as e:
        print(f"Ошибка сервера: {e}")
        sys.exit(1)
    
    finally:
        # Закрываем сокет
        server_socket.close()
        print("Сервер завершил работу")

if __name__ == "__main__":
    main()
