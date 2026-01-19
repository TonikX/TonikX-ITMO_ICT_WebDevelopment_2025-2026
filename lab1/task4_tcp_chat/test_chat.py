#!/usr/bin/env python3
"""
Тестовый скрипт для автоматического тестирования многопользовательского чата
"""

import socket
import threading
import time
import sys

class TestClient:
    def __init__(self, nickname, host='localhost', port=12347):
        self.nickname = nickname
        self.host = host
        self.port = port
        self.socket = None
        self.messages_received = []
        self.connected = False
        
    def connect(self):
        """Подключается к серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except Exception as e:
            print(f"❌ {self.nickname}: Ошибка подключения: {e}")
            return False
    
    def start(self):
        """Запускает тестового клиента"""
        if not self.connect():
            return
        
        print(f"✅ {self.nickname}: Подключен к серверу")
        
        # Получаем запрос на никнейм
        try:
            response = self.socket.recv(1024).decode('utf-8').strip()
            # Отправляем никнейм
            self.socket.send(self.nickname.encode('utf-8'))
            
            # Получаем подтверждение
            response = self.socket.recv(1024).decode('utf-8').strip()
            print(f"📝 {self.nickname}: {response}")
            
        except Exception as e:
            print(f"❌ {self.nickname}: Ошибка получения никнейма: {e}")
            return
        
        # Запускаем поток для получения сообщений
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        # Ждем немного для синхронизации
        time.sleep(0.5)
        
        # Отправляем тестовые сообщения
        self.send_message("Привет всем!")
        time.sleep(1)
        self.send_message("/users")
        time.sleep(1)
        self.send_message("/time")
        time.sleep(1)
        self.send_message("Пока!")
        
        # Ждем получения всех сообщений
        time.sleep(2)
        
        # Отключаемся
        self.disconnect()
    
    def receive_messages(self):
        """Получает сообщения от сервера"""
        try:
            while self.connected:
                try:
                    message = self.socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    
                    self.messages_received.append(message.strip())
                    print(f"📨 {self.nickname} получил: {message.strip()}")
                    
                except socket.error:
                    break
                except Exception as e:
                    print(f"❌ {self.nickname}: Ошибка получения сообщения: {e}")
                    break
        
        except Exception as e:
            print(f"❌ {self.nickname}: Ошибка потока получения: {e}")
    
    def send_message(self, message):
        """Отправляет сообщение серверу"""
        try:
            self.socket.send(message.encode('utf-8'))
            print(f"📤 {self.nickname} отправил: {message}")
        except Exception as e:
            print(f"❌ {self.nickname}: Ошибка отправки: {e}")
    
    def disconnect(self):
        """Отключается от сервера"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print(f"👋 {self.nickname}: Отключен")

def test_multiple_clients():
    """Тестирует подключение нескольких клиентов"""
    print("🧪 Тестирование многопользовательского чата")
    print("=" * 50)
    
    # Создаем тестовых клиентов
    clients = [
        TestClient("Alice"),
        TestClient("Bob"),
        TestClient("Charlie")
    ]
    
    # Запускаем клиентов в отдельных потоках
    threads = []
    for client in clients:
        thread = threading.Thread(target=client.start, daemon=True)
        threads.append(thread)
        thread.start()
        time.sleep(0.5)  # Небольшая задержка между подключениями
    
    # Ждем завершения всех потоков
    for thread in threads:
        thread.join(timeout=10)
    
    # Анализируем результаты
    print("\n📊 Результаты тестирования:")
    print("-" * 30)
    
    total_messages = 0
    for client in clients:
        message_count = len(client.messages_received)
        total_messages += message_count
        print(f"{client.nickname}: получил {message_count} сообщений")
    
    print(f"Всего сообщений получено: {total_messages}")
    
    if total_messages > 0:
        print("✅ Тест пройден: клиенты успешно обмениваются сообщениями")
    else:
        print("❌ Тест не пройден: сообщения не получены")

def main():
    print("🚀 Запуск тестов чата")
    print("Убедитесь, что сервер запущен на localhost:12347")
    print("Нажмите Enter для продолжения...")
    input()
    
    test_multiple_clients()

if __name__ == "__main__":
    main()
