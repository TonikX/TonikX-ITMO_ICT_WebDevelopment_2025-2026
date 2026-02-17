import socket


def run_client():
    try:
        sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Отправляем сообщение серверу
        message = 'Hello, server'
        server_address = ("localhost", 8080)

        print(f"Отправка сообщения серверу: {message}")
        sock_client.sendto(message.encode('utf-8'), server_address)

        # Получаем ответ от сервера
        response, address = sock_client.recvfrom(1024)
        print(f'Server {address}: {response.decode("utf-8")}')

    except Exception as e:
        print(f"Ошибка клиента: {e}")
    finally:
        sock_client.close()


if __name__ == "__main__":
    run_client()