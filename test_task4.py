#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование задания 4: Многопользовательский чат
"""

import socket
import threading
import time
import sys
from task4_chat import ChatServer

def test_client_connection(nickname, messages_to_send):
    """Тестовый клиент"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 12347))

        # Получение запроса никнейма
        response = client.recv(1024).decode('utf-8')
        if response == "NICK":
            client.send(nickname.encode('utf-8'))

        # Получение приветственного сообщения
        welcome = client.recv(1024).decode('utf-8')
        print(f"[{nickname}] Получено: {welcome}")

        # Отправка сообщений
        for msg in messages_to_send:
            time.sleep(1)
            client.send(msg.encode('utf-8'))
            print(f"[{nickname}] Отправлено: {msg}")

        time.sleep(2)
        client.close()
        print(f"[{nickname}] Отключился")

    except Exception as e:
        print(f"[{nickname}] Ошибка: {e}")

def run_test():
    """Запуск автоматического теста"""
    print("=== Автоматический тест чата ===")

    # Запуск сервера в отдельном потоке
    server = ChatServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)  # Ждем запуска сервера

    # Создание тестовых клиентов
    client1_messages = ["Привет всем!", "Как дела?", "Я первый клиент"]
    client2_messages = ["Привет!", "Все отлично!", "Я второй клиент"]
    client3_messages = ["Добро пожаловать!", "Отличный чат!", "Я третий"]

    # Запуск клиентов
    threading.Thread(target=test_client_connection, args=("Алиса", client1_messages)).start()
    time.sleep(0.5)
    threading.Thread(target=test_client_connection, args=("Боб", client2_messages)).start()
    time.sleep(0.5)
    threading.Thread(target=test_client_connection, args=("Карл", client3_messages)).start()

    # Ждем завершения теста
    time.sleep(10)
    print("\n=== Тест завершен ===")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "auto":
        run_test()
    else:
        print("Ручное тестирование:")
        print("1. python task4_chat.py server")
        print("2. python task4_chat.py client")
        print("")
        print("Автоматический тест:")
        print("python test_task4.py auto")