#!/usr/bin/env python3
"""
Задание 1: UDP клиент
Отправляет сообщение серверу и получает ответ
"""

import socket

def main():
    # Создаем UDP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Настройки сервера
    host = 'localhost'
    port = 9999
    server_address = (host, port)
    
    # Отправляем сообщение серверу
    message = "Hello, server"
    print(f"Отправка сообщения серверу: {message}")
    client_socket.sendto(message.encode('utf-8'), server_address)
    
    # Получаем ответ от сервера
    data, server = client_socket.recvfrom(1024)
    response = data.decode('utf-8')
    
    print(f"Получен ответ от сервера: {response}")
    
    # Закрываем сокет
    client_socket.close()

if __name__ == "__main__":
    main()
