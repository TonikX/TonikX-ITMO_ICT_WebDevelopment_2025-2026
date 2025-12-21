## Задание 3:

---
<b>Содержание:</b> Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html

<b>Требования:</b> Обязательно использовать библиотеку socket.

---
<b>Выполнение: </b>

1. Создаем скрипт для сервера
~~~python
import os
import socket

HOST = "localhost"
PORT = 8080
MAX_CONNECTIONS = 3
BUFFER_SIZE = 1024


def load_html_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding="utf-8") as file:
            return file.read()
    else:
        return None



def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)
    print("Server is running on http://localhost:8080")

    while True:
        client, _ = server.accept()
        client.recv(BUFFER_SIZE)

        html = load_html_file("index.html")
        if html is not None:
            html_bytes = html.encode("utf-8")
            response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        f"Content-Length: {len(html_bytes)}\r\n"
                        "\r\n"

            ).encode('utf-8') + html_bytes
        else:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "\r\n"
                "<h1>404 Not Found</h1>"
            ).encode('utf-8')
        client.sendall(response)
        client.close()

if __name__ == "__main__":
    run()
~~~
---
2. Проверяем что все работает
![img_3.png](screenshots%2Fimg_3.png)
