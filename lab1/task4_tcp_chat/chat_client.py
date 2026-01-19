#!/usr/bin/env python3
"""
TCP Chat Client для задания 4
Клиент для многопользовательского чата
"""

import socket
import sys
import threading
import time

class ChatClient:
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.socket = None
        self.nickname = None
        self.running = False
        
    def connect(self):
        """Подключается к серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.running = True
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к серверу: {e}")
            return False
    
    def start(self):
        """Запускает клиент"""
        if not self.connect():
            return
        
        print("🚀 Подключение к чат-серверу...")
        
        # Получаем никнейм
        self.nickname = self.get_nickname()
        if not self.nickname:
            print("❌ Не удалось получить никнейм")
            return
        
        print(f"✅ Подключен как {self.nickname}")
        print("💬 Начните общение! Введите /help для справки по командам")
        print("-" * 50)
        
        # Запускаем поток для получения сообщений
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        # Основной цикл для отправки сообщений
        try:
            while self.running:
                try:
                    message = input()
                    if not self.running:
                        break
                    
                    if message.strip():
                        self.send_message(message.strip())
                        
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
        except Exception as e:
            print(f"Ошибка ввода: {e}")
        
        finally:
            self.disconnect()
    
    def get_nickname(self):
        """Получает никнейм от пользователя"""
        try:
            # Получаем запрос на никнейм от сервера
            response = self.socket.recv(1024).decode('utf-8').strip()
            print(response)
            
            # Вводим никнейм
            nickname = input("> ").strip()
            
            # Отправляем никнейм серверу
            self.socket.send(nickname.encode('utf-8'))
            
            # Получаем подтверждение или ошибку
            response = self.socket.recv(1024).decode('utf-8').strip()
            print(response)
            
            # Если никнейм занят, повторяем
            if "уже занят" in response:
                return self.get_nickname()
            
            return nickname
            
        except Exception as e:
            print(f"Ошибка получения никнейма: {e}")
            return None
    
    def receive_messages(self):
        """Получает сообщения от сервера"""
        try:
            while self.running:
                try:
                    message = self.socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    
                    # Выводим сообщение
                    print(f"\r{message}")
                    print("> ", end="", flush=True)
                    
                except socket.error:
                    break
                except Exception as e:
                    print(f"\nОшибка получения сообщения: {e}")
                    break
        
        except Exception as e:
            print(f"Ошибка потока получения сообщений: {e}")
        
        finally:
            self.running = False
    
    def send_message(self, message):
        """Отправляет сообщение серверу"""
        try:
            self.socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
            self.running = False
    
    def disconnect(self):
        """Отключается от сервера"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("\n👋 Отключение от чата...")

def main():
    print("🎯 TCP Chat Client")
    print("=" * 30)
    
    # Можно указать адрес сервера
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = 'localhost'
    
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("❌ Неверный номер порта")
            return
    else:
        port = 12347
    
    client = ChatClient(host, port)
    
    try:
        client.start()
    except KeyboardInterrupt:
        print("\n🛑 Выход...")
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
