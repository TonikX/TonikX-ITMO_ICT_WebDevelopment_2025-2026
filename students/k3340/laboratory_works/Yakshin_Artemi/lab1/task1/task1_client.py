#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 1: UDP Клиент
Клиент отправляет "Hello, server" и получает "Hello, client"
"""

import socket

def main():
    # Создаем UDP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Адрес сервера
    server_address = ('localhost', 12345)
    
    try:
        # Отправляем сообщение серверу
        message = "Hello, server"
        client_socket.sendto(message.encode('utf-8'), server_address)
        print(f"Отправлено серверу: {message}")
        
        # Получаем ответ от сервера
        data, server_address = client_socket.recvfrom(1024)
        response = data.decode('utf-8')
        print(f"Получено от сервера: {response}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
