import socket

# AF_INET - IPv4, SOCK_STREAM - TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Решение проблемы Address already in use. Игнорирование состояния сокета TIME_WAIT
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp_socket.bind(('localhost', 9999))
tcp_socket.listen(5)


def create_http_response(body, status_code="200 OK", content_type="text/html"):
    body_bytes = body.encode('utf-8')

    response = f"HTTP/1.1 {status_code}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(body_bytes)}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"

    return response.encode('utf-8') + body_bytes

while True:
    client_socket, addr = tcp_socket.accept()
    print(f"Получено соединение от {addr}")

    try:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Запрос:\n{request.splitlines()[0]}")

        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        http_response = create_http_response(html_content)

        client_socket.sendall(http_response)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        client_socket.close()
        print(f"Соединение с {addr} закрыто")
