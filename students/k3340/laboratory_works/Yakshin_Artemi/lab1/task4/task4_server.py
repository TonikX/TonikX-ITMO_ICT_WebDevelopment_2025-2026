#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 4: Многопользовательский чат сервер
TCP сервер с поддержкой множественных клиентов через threading
"""

import socket
import threading
import time
from datetime import datetime

class ChatServer:
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start_server(self):
        """Запускает сервер"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Чат сервер запущен на {self.host}:{self.port}")
        print("Ожидание подключений...")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Подключен клиент: {address}")
                
                # Создаем поток для обработки клиента
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nСервер остановлен")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket, address):
        """Обрабатывает подключение клиента"""
        try:
            # Получаем никнейм
            nickname = client_socket.recv(1024).decode('utf-8')
            print(f"Получен никнейм: '{nickname}' от {address}")
            
            # Проверяем, не существует ли уже такой никнейм
            if nickname in self.nicknames:
                error_msg = "ERROR: Никнейм уже занят! Выберите другой."
                client_socket.send(error_msg.encode('utf-8'))
                print(f"Попытка подключения с занятым никнеймом '{nickname}' от {address}")
                # Закрываем соединение, чтобы клиент мог переподключиться
                client_socket.close()
                return
            
            # Добавляем клиента
            self.nicknames.append(nickname)
            self.clients.append(client_socket)
            
            print(f"Клиент {nickname} присоединился к чату")
            print(f"Активные пользователи: {', '.join(self.nicknames)}")
            
            # Отправляем подтверждение клиенту
            success_msg = "SUCCESS: Подключение успешно!"
            client_socket.send(success_msg.encode('utf-8'))
            print(f"Отправлено подтверждение клиенту {nickname}: {success_msg}")
            
            # Уведомляем всех о новом пользователе (кроме самого пользователя)
            # Отправляем системное сообщение только другим клиентам
            for client in self.clients:
                if client != client_socket:
                    try:
                        client.send(f"{nickname} присоединился к чату!".encode('utf-8'))
                    except:
                        pass
            
            while True:
                try:
                    # Получаем сообщение
                    message = client_socket.recv(1024).decode('utf-8')
                    
                    if message == "QUIT":
                        self.remove_client(client_socket, nickname)
                        break
                    
                    # Отправляем сообщение всем клиентам
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    full_message = f"[{timestamp}] {nickname}: {message}"
                    
                    # Выводим сообщение в терминал сервера
                    print(full_message)
                    
                    # Отправляем сообщение всем клиентам
                    self.broadcast(full_message, client_socket)
                    
                except ConnectionResetError:
                    self.remove_client(client_socket, nickname)
                    break
                    
        except Exception as e:
            print(f"Ошибка при обработке клиента {address}: {e}")
            self.remove_client(client_socket, nickname if 'nickname' in locals() else "Unknown")
    
    def broadcast(self, message, sender_socket):
        """Отправляет сообщение всем клиентам кроме отправителя"""
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    # Удаляем неактивного клиента
                    self.remove_client(client, "Unknown")
    
    def remove_client(self, client_socket, nickname):
        """Удаляет клиента из списка"""
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        if nickname in self.nicknames:
            self.nicknames.remove(nickname)
        
        print(f"Клиент {nickname} покинул чат")
        if self.nicknames:
            print(f"Активные пользователи: {', '.join(self.nicknames)}")
        else:
            print("В чате нет активных пользователей")
            
        # Уведомляем остальных клиентов о выходе
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(f"{nickname} покинул чат!".encode('utf-8'))
                except:
                    pass
        client_socket.close()

def main():
    server = ChatServer()
    server.start_server()

if __name__ == "__main__":
    main()
