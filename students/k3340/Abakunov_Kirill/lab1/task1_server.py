#!/usr/bin/env python3
"""
Задание 1: UDP сервер
Принимает сообщение от клиента и отправляет ответ
"""

import socket

def main():
    # Создаем UDP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Настройки сервера
    host = 'localhost'
    port = 9999
    
    # Привязываем сокет к адресу и порту
    server_socket.bind((host, port))
    
    print(f"UDP сервер запущен на {host}:{port}")
    print("Ожидание сообщений от клиентов...\n")
    
    while True:
        # Получаем данные от клиента
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')
        
        print(f"Получено от {client_address}: {message}")
        
        # Отправляем ответ клиенту
        response = "Hello, client"
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Отправлено клиенту: {response}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
