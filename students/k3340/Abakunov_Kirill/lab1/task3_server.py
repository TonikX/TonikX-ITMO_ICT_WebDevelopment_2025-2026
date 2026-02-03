#!/usr/bin/env python3
"""
Задание 3: HTTP сервер
Отдает HTML-страницу из файла index.html
"""

import socket
import os

def main():
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Позволяем переиспользовать адрес
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Настройки сервера
    host = 'localhost'
    port = 8080
    
    # Привязываем сокет к адресу и порту
    server_socket.bind((host, port))
    
    # Начинаем прослушивание
    server_socket.listen(5)
    
    print(f"HTTP сервер запущен на http://{host}:{port}")
    print("Откройте браузер и перейдите по указанному адресу")
    print("Для остановки нажмите Ctrl+C\n")
    
    while True:
        try:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"Подключение от {client_address}")
            
            # Получаем HTTP-запрос
            request = client_socket.recv(1024).decode('utf-8')
            print(f"Запрос:\n{request[:200]}...\n")
            
            # Читаем HTML-файл
            html_file_path = os.path.join(os.path.dirname(__file__), 'index.html')
            
            try:
                with open(html_file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                
                # Формируем HTTP-ответ
                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type: text/html; charset=utf-8\r\n"
                response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
                response += "Connection: close\r\n"
                response += "\r\n"
                response += html_content
                
                # Отправляем ответ
                client_socket.send(response.encode('utf-8'))
                print("HTML-страница отправлена клиенту\n")
                
            except FileNotFoundError:
                # Если файл не найден, отправляем ошибку 404
                response = "HTTP/1.1 404 Not Found\r\n"
                response += "Content-Type: text/html; charset=utf-8\r\n"
                response += "\r\n"
                response += "<h1>404 - File Not Found</h1>"
                response += "<p>Файл index.html не найден</p>"
                client_socket.send(response.encode('utf-8'))
                print("Ошибка: файл index.html не найден\n")
            
            # Закрываем соединение с клиентом
            client_socket.close()
            
        except Exception as e:
            print(f"Ошибка: {e}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
