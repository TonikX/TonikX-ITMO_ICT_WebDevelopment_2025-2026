# Задание
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее
HTML-страницу, которая сервер подгружает из файла index.html.

**Требования:**

- Обязательно использовать библиотеку socket.
 
***

# Решение

## Сервер

```python
import socket

HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f'Сервер запущен на {HOST}:{PORT}')

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение. {client_address}')

    try:
        # HTML
        with open('index.html', 'rb') as html_file:
            html_content = html_file.read()

        # Header
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html_content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode('utf-8')

        client_connection.sendall(headers + html_content)

    except:
        print('Ошибка ответа')

    client_connection.close()

```
## Сервер

```python
import socket

HOST = '127.0.0.1'
PORT = 9090


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except:
        print("Сервер недоступен.")
        return False

    print('Подключение к серверу установлено')

    # Формирование запроса
    http_request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"

    try:
        client_socket.sendall(http_request.encode('utf-8'))

        # Получение ответа
        response = b""
        while True:
            try:
                part = client_socket.recv(1024)
                if not part:
                    break
                response += part
            except socket.error as e:
                break

        print(response.decode('utf-8'))

    except Exception as e:
        print(f"Ошибка при запросе: {e}")

    client_socket.close()


if __name__ == '__main__':
    main()
```

***

# Пояснение

Создаём TCP сокет на сервере, используя адрес `127.0.0.1` и порт `9090` и устанавливаем соединение с клиентом.
Далее считываем файл index.html, формируем ответ `200 OK` и отправляем его клиенту.

Браузер отправляет HTTP GET запрос серверу и получает в ответ HTTP-сообщение, содержащее
HTML-страницу index.html.