#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 3: HTTP Сервер
Клиент подключается к серверу, и в ответ получает HTTP-сообщение,
содержащее HTML-страницу, которая сервер подгружает из файла index.html
"""

import socket
import sys
import os
import threading
import time

def create_html_file():
    """Создание HTML файла для демонстрации"""
    html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Добро пожаловать!</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .info {
            background-color: #e7f3ff;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature {
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Добро пожаловать на наш сайт!</h1>
        
        <div class="info">
            <h2>О проекте</h2>
            <p>Это демонстрационная HTML-страница, загружаемая через HTTP-сервер, 
            реализованный с помощью библиотеки socket в Python.</p>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🚀 Производительность</h3>
                <p>Быстрая обработка HTTP-запросов</p>
            </div>
            <div class="feature">
                <h3>🔧 Простота</h3>
                <p>Легкая настройка и использование</p>
            </div>
            <div class="feature">
                <h3>📚 Обучение</h3>
                <p>Отличный пример для изучения сокетов</p>
            </div>
        </div>
        
        <div class="info">
            <h2>Технические детали</h2>
            <ul>
                <li>Протокол: HTTP/1.1</li>
                <li>Порт: 8080</li>
                <li>Реализация: Python socket</li>
                <li>Кодировка: UTF-8</li>
            </ul>
        </div>
        
        <footer style="text-align: center; margin-top: 40px; color: #666;">
            <p>Страница загружена через самодельный HTTP-сервер</p>
        </footer>
    </div>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("HTML файл index.html создан")

def http_server():
    """HTTP сервер для задания 3"""
    print("=== HTTP Сервер ===")
    
    # Создание HTML файла если его нет
    if not os.path.exists('index.html'):
        create_html_file()
    
    # Создание TCP сокета для HTTP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('localhost', 8080))
        server_socket.listen(1)
        print("HTTP сервер запущен на порту 8080")
        print("Откройте http://localhost:8080/ в браузере")
        print("Ожидание подключений...")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Подключен клиент: {addr}")
            
            try:
                # Получение HTTP запроса
                request = client_socket.recv(1024).decode('utf-8')
                print(f"Запрос: {request.split('\\n')[0]}")
                
                # Парсинг HTTP запроса
                request_lines = request.split('\\n')
                if request_lines:
                    request_line = request_lines[0]
                    parts = request_line.split()
                    if len(parts) >= 3:
                        method, path, version = parts[0], parts[1], parts[2]
                        
                        if method == 'GET' and path == '/':
                            # Чтение HTML файла
                            try:
                                with open('index.html', 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                                
                                # Формирование HTTP ответа
                                response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html_content.encode('utf-8'))}
Connection: close

{html_content}"""
                                
                                client_socket.send(response.encode('utf-8'))
                                print("Отправлен HTML файл")
                                
                            except FileNotFoundError:
                                # Обработка ошибки 404
                                error_response = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8
Connection: close

<h1>404 Not Found</h1>
<p>Файл index.html не найден</p>"""
                                client_socket.send(error_response.encode('utf-8'))
                        else:
                            # Обработка других путей
                            error_response = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8
Connection: close

<h1>404 Not Found</h1>"""
                            client_socket.send(error_response.encode('utf-8'))
                
            except Exception as e:
                print(f"Ошибка обработки запроса: {e}")
            finally:
                client_socket.close()
                
    except KeyboardInterrupt:
        print("\\nСервер остановлен пользователем")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        server_socket.close()

def http_client():
    """HTTP клиент для задания 3"""
    print("=== HTTP Клиент ===")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(('localhost', 8080))
        
        # Формирование HTTP GET запроса
        request = "GET / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n"
        client_socket.send(request.encode('utf-8'))
        
        # Получение HTTP ответа
        response = client_socket.recv(4096).decode('utf-8')
        print("HTTP ответ:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
    except Exception as e:
        print(f"Ошибка клиента: {e}")
    finally:
        client_socket.close()

def run_demo():
    """Демонстрация работы HTTP сервера"""
    print("=== Демонстрация HTTP Сервер ===")
    
    # Запуск сервера в отдельном потоке
    server_thread = threading.Thread(target=http_server, daemon=True)
    server_thread.start()
    
    # Небольшая задержка для запуска сервера
    time.sleep(2)
    
    # Запуск клиента
    http_client()
    
    # Ожидание завершения
    time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            http_server()
        elif sys.argv[1] == "client":
            http_client()
        elif sys.argv[1] == "demo":
            run_demo()
        else:
            print("Использование: python task3_http_server.py [server|client|demo]")
    else:
        print("Использование:")
        print("  python task3_http_server.py server  - запустить сервер")
        print("  python task3_http_server.py client  - запустить клиент")
        print("  python task3_http_server.py demo    - демонстрация")
        print("  Откройте http://localhost:8080/ в браузере для просмотра")
