import socket
import os

# Создаем TCP сокет для HTTP сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Позволяем переиспользовать адрес
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Указываем адрес и порт для сервера
server_address = ('localhost', 8080)
server_socket.bind(server_address)

# Начинаем прослушивание
server_socket.listen(5)

print("HTTP сервер запущен на http://localhost:8080")
print("Ожидание подключений...")

def load_html_file():
    """Загружает содержимое index.html файла"""
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<html><body><h1>Ошибка: index.html не найден</h1></body></html>"

def create_http_response(html_content):
    """Создает HTTP ответ с HTML содержимым"""
    # HTTP заголовки
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"  # Пустая строка между заголовками и телом
    response += html_content
    
    return response

while True:
    try:
        # Ждем подключения клиента
        client_socket, client_address = server_socket.accept()
        print(f"Подключился клиент: {client_address}")
        
        # Получаем HTTP запрос от клиента
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Получен запрос:\n{request[:200]}...")  # Показываем первые 200 символов
        
        # Загружаем HTML содержимое из файла
        html_content = load_html_file()
        
        # Создаем HTTP ответ
        response = create_http_response(html_content)
        
        # Отправляем ответ клиенту
        client_socket.send(response.encode('utf-8'))
        print(f"Отправлен HTTP ответ клиенту {client_address}")
        
        # Закрываем соединение с клиентом
        client_socket.close()
        print("Соединение закрыто\n")
        
    except KeyboardInterrupt:
        print("\nЗавершение работы сервера...")
        break
    except Exception as e:
        print(f"Ошибка при обработке клиента: {e}")

# Закрываем серверный сокет
server_socket.close()
print("Сервер остановлен.")
