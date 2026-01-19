#!/usr/bin/env python3
"""
HTTP Server для задания 3
Реализует простой веб-сервер с использованием библиотеки socket
Отдает HTML-страницу из файла index.html
"""

import socket
import sys
import os
from datetime import datetime

def get_content_type(file_path):
    """Определяет Content-Type по расширению файла"""
    if file_path.endswith('.html'):
        return 'text/html; charset=utf-8'
    elif file_path.endswith('.css'):
        return 'text/css'
    elif file_path.endswith('.js'):
        return 'application/javascript'
    elif file_path.endswith('.png'):
        return 'image/png'
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        return 'image/jpeg'
    elif file_path.endswith('.gif'):
        return 'image/gif'
    else:
        return 'text/plain'

def read_file(file_path):
    """Читает содержимое файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка чтения файла {file_path}: {e}")
        return None

def create_http_response(status_code, content_type, content, additional_headers=None):
    """Создает HTTP-ответ"""
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error"
    }
    
    status_line = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
    
    headers = [
        f"Content-Type: {content_type}\r\n",
        f"Content-Length: {len(content.encode('utf-8'))}\r\n",
        f"Server: Python-HTTP-Server/1.0\r\n",
        f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n",
        "Connection: close\r\n"
    ]
    
    if additional_headers:
        headers.extend(additional_headers)
    
    response = status_line + "".join(headers) + "\r\n" + content
    return response

def handle_request(request):
    """Обрабатывает HTTP-запрос"""
    try:
        # Парсим первую строку запроса
        lines = request.split('\n')
        if not lines:
            return create_http_response(400, 'text/plain', 'Bad Request')
        
        request_line = lines[0].strip()
        parts = request_line.split()
        
        if len(parts) < 3:
            return create_http_response(400, 'text/plain', 'Bad Request')
        
        method, path, version = parts[0], parts[1], parts[2]
        
        # Проверяем метод
        if method != 'GET':
            return create_http_response(405, 'text/plain', 'Method Not Allowed')
        
        # Обрабатываем путь
        if path == '/' or path == '/index.html':
            file_path = 'index.html'
        else:
            # Убираем ведущий слеш
            file_path = path.lstrip('/')
        
        # Читаем файл
        content = read_file(file_path)
        
        if content is None:
            # Файл не найден
            error_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>404 - Not Found</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
                    h1 { color: #e74c3c; }
                </style>
            </head>
            <body>
                <h1>404 - Страница не найдена</h1>
                <p>Запрашиваемый файл не найден на сервере.</p>
                <a href="/">Вернуться на главную</a>
            </body>
            </html>
            """
            return create_http_response(404, 'text/html; charset=utf-8', error_content)
        
        # Определяем Content-Type
        content_type = get_content_type(file_path)
        
        # Создаем успешный ответ
        return create_http_response(200, content_type, content)
        
    except Exception as e:
        print(f"Ошибка обработки запроса: {e}")
        error_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>500 - Server Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }}
                h1 {{ color: #e74c3c; }}
            </style>
        </head>
        <body>
            <h1>500 - Внутренняя ошибка сервера</h1>
            <p>Произошла ошибка при обработке запроса.</p>
        </body>
        </html>
        """
        return create_http_response(500, 'text/html; charset=utf-8', error_content)

def main():
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Настройки сервера
    host = 'localhost'
    port = 8080
    
    try:
        # Позволяем переиспользовать адрес
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Привязываем сокет к адресу и порту
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"HTTP Server запущен на http://{host}:{port}")
        print("Сервер готов к обработке запросов...")
        print("Нажмите Ctrl+C для остановки сервера")
        print("-" * 50)
        
        while True:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"Подключение от: {client_address}")
            
            try:
                # Получаем запрос от клиента
                request = client_socket.recv(1024).decode('utf-8')
                
                if request:
                    first_line = request.split('\n')[0]
                    print(f"Запрос: {first_line}")
                    
                    # Обрабатываем запрос
                    response = handle_request(request)
                    
                    # Отправляем ответ клиенту
                    client_socket.send(response.encode('utf-8'))
                    print(f"Ответ отправлен клиенту {client_address}")
                
            except Exception as e:
                print(f"Ошибка обработки клиента {client_address}: {e}")
            
            finally:
                # Закрываем соединение с клиентом
                client_socket.close()
                print(f"Соединение с {client_address} закрыто")
                print("-" * 30)
    
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
        sys.exit(1)
    
    finally:
        # Закрываем серверный сокет
        server_socket.close()
        print("Сервер завершил работу")

if __name__ == "__main__":
    main()
