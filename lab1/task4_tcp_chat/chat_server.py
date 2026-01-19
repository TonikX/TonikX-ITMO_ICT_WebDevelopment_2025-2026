#!/usr/bin/env python3
"""
TCP Chat Server для задания 4
Многопользовательский чат с использованием threading
"""

import socket
import sys
import threading
import time
from datetime import datetime

class ChatServer:
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.clients = {}  # {client_socket: {'nickname': str, 'address': tuple}}
        self.server_socket = None
        self.running = False
        self.lock = threading.Lock()
        
    def start(self):
        """Запускает сервер"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            
            self.running = True
            print(f"🚀 Chat Server запущен на {self.host}:{self.port}")
            print("Ожидание подключений...")
            print("Нажмите Ctrl+C для остановки сервера")
            print("-" * 50)
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"📱 Новое подключение от {client_address}")
                    
                    # Создаем поток для обработки клиента
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error:
                    if self.running:
                        print("Ошибка при принятии подключения")
                    break
                    
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Останавливает сервер"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        # Закрываем все клиентские соединения
        with self.lock:
            for client_socket in list(self.clients.keys()):
                try:
                    client_socket.close()
                except:
                    pass
            self.clients.clear()
        
        print("🛑 Сервер остановлен")
    
    def handle_client(self, client_socket, client_address):
        """Обрабатывает подключение клиента"""
        nickname = None
        
        try:
            # Получаем никнейм от клиента
            nickname = self.get_nickname(client_socket, client_address)
            if not nickname:
                return
            
            # Добавляем клиента в список
            with self.lock:
                self.clients[client_socket] = {
                    'nickname': nickname,
                    'address': client_address
                }
            
            # Уведомляем всех о новом пользователе
            self.broadcast(f"👋 {nickname} присоединился к чату!", exclude=client_socket)
            self.send_to_client(client_socket, f"✅ Добро пожаловать в чат, {nickname}!")
            self.send_to_client(client_socket, f"📊 Пользователей онлайн: {len(self.clients)}")
            
            print(f"👤 {nickname} ({client_address}) подключился. Всего пользователей: {len(self.clients)}")
            
            # Обрабатываем сообщения от клиента
            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    
                    message = message.strip()
                    if not message:
                        continue
                    
                    # Обрабатываем команды
                    if message.startswith('/'):
                        self.handle_command(client_socket, nickname, message)
                    else:
                        # Обычное сообщение
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        formatted_message = f"[{timestamp}] {nickname}: {message}"
                        self.broadcast(formatted_message, exclude=client_socket)
                        print(f"💬 {nickname}: {message}")
                
                except socket.error:
                    break
                except Exception as e:
                    print(f"Ошибка обработки сообщения от {nickname}: {e}")
                    break
        
        except Exception as e:
            print(f"Ошибка обработки клиента {client_address}: {e}")
        
        finally:
            # Удаляем клиента из списка
            if nickname:
                with self.lock:
                    if client_socket in self.clients:
                        del self.clients[client_socket]
                
                # Уведомляем всех об отключении
                self.broadcast(f"👋 {nickname} покинул чат!")
                print(f"👤 {nickname} ({client_address}) отключился. Осталось пользователей: {len(self.clients)}")
            
            try:
                client_socket.close()
            except:
                pass
    
    def get_nickname(self, client_socket, client_address):
        """Получает никнейм от клиента"""
        try:
            # Отправляем запрос на никнейм
            self.send_to_client(client_socket, "Введите ваш никнейм:")
            
            # Получаем никнейм
            nickname = client_socket.recv(1024).decode('utf-8').strip()
            
            if not nickname:
                return None
            
            # Проверяем уникальность никнейма
            with self.lock:
                existing_nicknames = [client['nickname'] for client in self.clients.values()]
                if nickname in existing_nicknames:
                    self.send_to_client(client_socket, f"❌ Никнейм '{nickname}' уже занят. Попробуйте другой.")
                    return self.get_nickname(client_socket, client_address)
            
            return nickname
            
        except Exception as e:
            print(f"Ошибка получения никнейма от {client_address}: {e}")
            return None
    
    def handle_command(self, client_socket, nickname, command):
        """Обрабатывает команды чата"""
        command = command.lower().strip()
        
        if command == '/help':
            help_text = """
📋 Доступные команды:
/help - показать эту справку
/users - список пользователей онлайн
/time - текущее время
/quit - покинуть чат
            """
            self.send_to_client(client_socket, help_text)
        
        elif command == '/users':
            with self.lock:
                users = [client['nickname'] for client in self.clients.values()]
            users_text = f"👥 Пользователи онлайн ({len(users)}): {', '.join(users)}"
            self.send_to_client(client_socket, users_text)
        
        elif command == '/time':
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.send_to_client(client_socket, f"🕐 Текущее время: {current_time}")
        
        elif command == '/quit':
            self.send_to_client(client_socket, "👋 До свидания!")
            client_socket.close()
        
        else:
            self.send_to_client(client_socket, f"❌ Неизвестная команда: {command}. Введите /help для справки.")
    
    def send_to_client(self, client_socket, message):
        """Отправляет сообщение конкретному клиенту"""
        try:
            client_socket.send(f"{message}\n".encode('utf-8'))
        except:
            pass
    
    def broadcast(self, message, exclude=None):
        """Отправляет сообщение всем клиентам, кроме исключенного"""
        with self.lock:
            for client_socket in list(self.clients.keys()):
                if client_socket != exclude:
                    self.send_to_client(client_socket, message)

def main():
    server = ChatServer()
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n🛑 Получен сигнал остановки...")
        server.stop()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        server.stop()
        sys.exit(1)

if __name__ == "__main__":
    main()
