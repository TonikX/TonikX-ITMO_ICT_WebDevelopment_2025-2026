#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 4: Многопользовательский чат клиент
TCP клиент для подключения к чат серверу
"""

import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""
        
    def connect(self):
        """Подключается к серверу"""
        try:
            self.client_socket.connect((self.host, self.port))
            print("Подключен к чат серверу")
            
            # Получаем никнейм с проверкой
            while True:
                self.nickname = input("Введите ваш никнейм: ")
                self.client_socket.send(self.nickname.encode('utf-8'))
                
                try:
                    # Проверяем ответ сервера
                    print(f"Ожидаем ответ от сервера для никнейма '{self.nickname}'...")
                    response = self.client_socket.recv(1024).decode('utf-8')
                    print(f"Получен ответ: '{response}'")
                    
                    if response.startswith("ERROR:"):
                        print(response)
                        print("Попробуйте другой никнейм.")
                        continue
                    elif response.startswith("SUCCESS:"):
                        print(f"Добро пожаловать, {self.nickname}!")
                        break
                    else:
                        # Если получили неожиданный ответ, попробуем еще раз
                        print(f"Получен неожиданный ответ: {response}")
                        print("Попробуйте еще раз.")
                        continue
                except ConnectionResetError:
                    print("Соединение с сервером потеряно. Попробуйте переподключиться.")
                    return
                except ConnectionAbortedError:
                    print("Соединение с сервером прервано. Попробуйте переподключиться.")
                    return
                except Exception as e:
                    print(f"Ошибка при получении ответа: {e}")
                    return
            
            # Запускаем поток для получения сообщений
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Основной цикл для отправки сообщений
            self.send_messages()
            
        except Exception as e:
            print(f"Ошибка подключения: {e}")
        finally:
            self.client_socket.close()
    
    def receive_messages(self):
        """Получает сообщения от сервера"""
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                # Игнорируем служебные сообщения SUCCESS и ERROR
                if not message.startswith("SUCCESS:") and not message.startswith("ERROR:"):
                    print(message)
            except:
                print("Соединение с сервером потеряно")
                break
    
    def send_messages(self):
        """Отправляет сообщения на сервер"""
        print("Начните общение! Введите 'QUIT' для выхода")
        while True:
            try:
                message = input()
                if message.upper() == 'QUIT':
                    self.client_socket.send('QUIT'.encode('utf-8'))
                    break
                self.client_socket.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                self.client_socket.send('QUIT'.encode('utf-8'))
                break
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                break

def main():
    client = ChatClient()
    client.connect()

if __name__ == "__main__":
    main()
