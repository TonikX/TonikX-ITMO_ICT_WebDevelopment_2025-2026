#!/usr/bin/env python3
"""
Задание 4: Клиент для многопользовательского чата
Подключается к серверу и обменивается сообщениями
"""

import socket
import threading
import sys

def receive_messages(client_socket):
    """Получает сообщения от сервера"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\r{message}\n>>> ", end='', flush=True)
        except:
            break

def send_messages(client_socket):
    """Отправляет сообщения серверу"""
    while True:
        try:
            message = input(">>> ")
            if message.lower() in ['exit', 'quit', 'выход']:
                print("Отключение от чата...")
                break
            if message.strip():
                client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            break

def main():
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Настройки сервера
    host = 'localhost'
    port = 9997
    
    try:
        # Подключаемся к серверу
        print(f"Подключение к серверу {host}:{port}...")
        client_socket.connect((host, port))
        print("Успешное подключение!")
        print("-" * 50)
        
        # Получаем приглашение ввести имя
        prompt = client_socket.recv(1024).decode('utf-8')
        username = input(prompt)
        client_socket.send(username.encode('utf-8'))
        
        # Получаем приветственное сообщение
        welcome = client_socket.recv(1024).decode('utf-8')
        print(welcome)
        print("-" * 50)
        print("Команды: 'exit', 'quit', 'выход' - выйти из чата")
        print("-" * 50)
        
        # Создаем поток для получения сообщений
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # Основной поток для отправки сообщений
        send_messages(client_socket)
        
    except ConnectionRefusedError:
        print("Ошибка: не удалось подключиться к серверу.")
        print("Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()
        print("Отключено от сервера.")
        sys.exit(0)

if __name__ == "__main__":
    main()
