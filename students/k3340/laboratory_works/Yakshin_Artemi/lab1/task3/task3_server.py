#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 3: HTTP Сервер
Сервер возвращает HTML страницу из файла index.html
"""

import socket
import os
from datetime import datetime

def load_html_file(filename):
    """Загружает HTML файл"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return """
        <html>
        <head><title>Ошибка</title></head>
        <body>
            <h1>Ошибка 404</h1>
            <p>Файл index.html не найден</p>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <head><title>Ошибка</title></head>
        <body>
            <h1>Ошибка сервера</h1>
            <p>{str(e)}</p>
        </body>
        </html>
        """

def load_css_file(filename):
    """Загружает CSS файл"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "/* CSS файл не найден */"
    except Exception as e:
        return f"/* Ошибка загрузки CSS: {str(e)} */"

def create_http_response(content, content_type="text/html"):
    """Создает HTTP ответ"""
    response = f"""HTTP/1.1 200 OK
Content-Type: {content_type}; charset=utf-8
Content-Length: {len(content.encode('utf-8'))}
Connection: close
Server: Python Socket Server

{content}"""
    return response

def get_404_response():
    """Создает 404 ответ"""
    content = """
    <html>
    <head><title>404 Not Found</title></head>
    <body>
        <h1>404 Not Found</h1>
        <p>Запрашиваемый ресурс не найден</p>
    </body>
    </html>
    """
    response = f"""HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8
Content-Length: {len(content.encode('utf-8'))}
Connection: close
Server: Python Socket Server

{content}"""
    return response

def main():
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)
    server_socket.listen(5)
    
    print(f"HTTP сервер запущен на http://{server_address[0]}:{server_address[1]}")
    print("Ожидание подключений...")
    
    # Загружаем HTML файл
    # Определяем путь к файлам относительно скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(script_dir, 'index.html')
    css_file = os.path.join(script_dir, 'style.css')
    
    print(f"Текущая рабочая директория: {os.getcwd()}")
    print(f"Папка скрипта: {script_dir}")
    print(f"HTML файл: {html_file}")
    print(f"CSS файл: {css_file}")
    
    html_content = load_html_file(html_file)
    
    try:
        while True:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")
            
            try:
                # Получаем HTTP запрос
                request = client_socket.recv(1024).decode('utf-8')
                print(f"Получен запрос от {client_address}")
                print(f"Запрос: {request[:200]}...")
                
                # Парсим запрос
                lines = request.split('\n')
                if lines and len(lines[0].split()) >= 3:
                    try:
                        request_line = lines[0]
                        method, path, _ = request_line.split(' ', 2)
                        
                        if path == '/style.css':
                            # Отправляем CSS файл
                            css_content = load_css_file(css_file)
                            http_response = create_http_response(css_content, "text/css")
                            print(f"Отправлен CSS файл клиенту {client_address}")
                        elif path == '/' or path == '/index.html':
                            # Отправляем HTML страницу
                            http_response = create_http_response(html_content)
                            print(f"Отправлен HTML ответ клиенту {client_address}")
                        else:
                            # 404 ошибка для неизвестных путей
                            http_response = get_404_response()
                            print(f"404 ошибка для пути {path} клиенту {client_address}")
                    except ValueError:
                        # Если не удается распарсить запрос, отправляем HTML
                        http_response = create_http_response(html_content)
                        print(f"Ошибка парсинга запроса, отправлен HTML клиенту {client_address}")
                else:
                    http_response = create_http_response(html_content)
                
                # Отправляем ответ
                client_socket.send(http_response.encode('utf-8'))
                
            except Exception as e:
                print(f"Ошибка при обработке клиента: {e}")
            finally:
                client_socket.close()
                print(f"Соединение с {client_address} закрыто")
                
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
