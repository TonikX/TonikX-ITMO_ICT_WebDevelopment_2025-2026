#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 1: UDP Hello
Клиент отправляет серверу сообщение «Hello, server», 
сервер отвечает «Hello, client»
"""

import socket
import sys
import threading
import time

def udp_server():
    """UDP сервер для задания 1"""
    print("=== UDP Сервер ===")
 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        server_socket.bind(('localhost', 12345))
        print("UDP сервер запущен на порту 12345")
        print("Ожидание сообщений...")
        
        while True:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"Получено от {addr}: {message}")
            
            if message == "Hello, server":
                response = "Hello, client"
                server_socket.sendto(response.encode('utf-8'), addr)
                print(f"Отправлено: {response}")
            else:
                print(f"Неожиданное сообщение: {message}")
                
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        server_socket.close()

def udp_client():
    """UDP клиент для задания 1"""
    print("=== UDP Клиент ===")
    
    # Создание UDP сокета
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Отправка сообщения серверу
        message = "Hello, server"
        client_socket.sendto(message.encode('utf-8'), ('localhost', 12345))
        print(f"Отправлено: {message}")
        
        # Получение ответа от сервера
        response, addr = client_socket.recvfrom(1024)
        print(f"Получено от {addr}: {response.decode('utf-8')}")
        
    except Exception as e:
        print(f"Ошибка клиента: {e}")
    finally:
        client_socket.close()

def run_demo():
    """Демонстрация работы UDP клиент-сервера"""
    print("=== Демонстрация UDP Hello ===")
    
    # Запуск сервера в отдельном потоке
    server_thread = threading.Thread(target=udp_server, daemon=True)
    server_thread.start()
    
    # Небольшая задержка для запуска сервера
    time.sleep(1)
    
    # Запуск клиента
    udp_client()
    
    # Ожидание завершения
    time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            udp_server()
        elif sys.argv[1] == "client":
            udp_client()
        elif sys.argv[1] == "demo":
            run_demo()
        else:
            print("Использование: python task1_udp_hello.py [server|client|demo]")
    else:
        print("Использование:")
        print("  python task1_udp_hello.py server  - запустить сервер")
        print("  python task1_udp_hello.py client  - запустить клиент")
        print("  python task1_udp_hello.py demo    - демонстрация")
