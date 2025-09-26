#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 4: Многопользовательский чат
Многопользовательский чат с поддержкой нескольких клиентов через TCP и threading
"""

import socket
import sys
import threading
import time
from datetime import datetime

class ChatServer:
    """Класс многопользовательского чат сервера"""
    
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start(self):
        """Запуск чат сервера"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"=== Многопользовательский Чат Сервер ===")
            print(f"Сервер запущен на {self.host}:{self.port}")
            print("Ожидание подключений...")
            
            while True:
                # Принятие нового подключения
                client_socket, address = self.server_socket.accept()
                print(f"Подключен клиент: {address}")
                
                # Запрос никнейма
                client_socket.send("NICK".encode('utf-8'))
                nickname = client_socket.recv(1024).decode('utf-8')
                
                # Добавление клиента в списки
                self.nicknames.append(nickname)
                self.clients.append(client_socket)
                
                print(f"Никнейм клиента: {nickname}")
                
                # Уведомление всех о новом пользователе
                self.broadcast(f"{nickname} присоединился к чату!")
                
                # Приветственное сообщение новому клиенту
                client_socket.send("Подключен к серверу!".encode('utf-8'))
                
                # Запуск потока для обработки клиента
                thread = threading.Thread(target=self.handle_client, args=(client_socket, nickname))
                thread.start()
                
        except KeyboardInterrupt:
            print("\nСервер остановлен пользователем")
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            self.server_socket.close()
    
    def broadcast(self, message):
        """Отправка сообщения всем клиентам"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        for client in self.clients:
            try:
                client.send(formatted_message.encode('utf-8'))
            except:
                # Удаление отключенного клиента
                self.remove_client(client)
    
    def handle_client(self, client, nickname):
        """Обработка сообщений от клиента"""
        while True:
            try:
                message = client.recv(1024)
                if message:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    formatted_message = f"[{timestamp}] {nickname}: {message.decode('utf-8')}"
                    self.broadcast(formatted_message)
                    print(f"Сообщение от {nickname}: {message.decode('utf-8')}")
                else:
                    self.remove_client(client)
                    break
            except:
                self.remove_client(client)
                break
    
    def remove_client(self, client):
        """Удаление клиента из чата"""
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            
            # Уведомление о выходе пользователя
            self.broadcast(f"{nickname} покинул чат!")
            print(f"Клиент {nickname} отключился")
            client.close()

class ChatClient:
    """Класс чат клиента"""
    
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None
        
    def connect(self, nickname):
        """Подключение к чат серверу"""
        try:
            self.client_socket.connect((self.host, self.port))
            self.nickname = nickname
            
            # Отправка никнейма
            self.client_socket.send(nickname.encode('utf-8'))
            
            # Запуск потока для получения сообщений
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Запуск отправки сообщений
            self.send()
            
        except Exception as e:
            print(f"Ошибка подключения: {e}")
    
    def receive(self):
        """Получение сообщений от сервера"""
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                print(message)
            except:
                print("Ошибка получения сообщения")
                self.client_socket.close()
                break
    
    def send(self):
        """Отправка сообщений на сервер"""
        while True:
            try:
                message = input()
                if message.lower() == 'quit':
                    self.client_socket.close()
                    break
                self.client_socket.send(message.encode('utf-8'))
            except:
                break

def run_server():
    """Запуск сервера"""
    server = ChatServer()
    server.start()

def run_client():
    """Запуск клиента"""
    nickname = input("Введите ваш никнейм: ")
    client = ChatClient()
    client.connect(nickname)

def run_demo():
    """Демонстрация работы чата"""
    print("Инструкция по тестированию:")
    print("1. Запустите сервер: python task4_chat.py server")
    print("2. В другом терминале запустите клиент: python task4_chat.py client")
    print("3. Повторите шаг 2 для дополнительных клиентов")
    print("4. Введите никнеймы и отправляйте сообщения")
    print("5. Введите 'quit' для выхода из клиента")
    print("Нажмите Enter для запуска сервера...")
    input()
    
    # Запуск сервера
    run_server()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            run_server()
        elif sys.argv[1] == "client":
            run_client()
        elif sys.argv[1] == "demo":
            run_demo()
        else:
            print("Использование: python task4_chat.py [server|client|demo]")
    else:
        print("Использование:")
        print("  python task4_chat.py server  - запустить сервер")
        print("  python task4_chat.py client  - запустить клиент")
        print("  python task4_chat.py demo    - демонстрация")
        print("")
        print("Для тестирования чата:")
        print("1. Запустите сервер: python task4_chat.py server")
        print("2. В другом терминале запустите клиент: python task4_chat.py client")
        print("3. Повторите шаг 2 для дополнительных клиентов")
