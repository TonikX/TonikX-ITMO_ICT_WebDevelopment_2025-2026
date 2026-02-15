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