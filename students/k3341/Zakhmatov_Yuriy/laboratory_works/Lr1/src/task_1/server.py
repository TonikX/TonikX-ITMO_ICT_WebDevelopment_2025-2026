import socket


def run():
    # Создание UDP сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Задаем параметры
    server_address = ("localhost", 8080)
    server_socket.bind(server_address)

    print(f"Server started on {server_address[0]}:{server_address[1]}")
    print("Awaiting connection...")

    try:
        while True:
            # Получаем запрос клиента

            data, client_address = server_socket.recvfrom(1024)
            message = data.decode("utf-8")

            print(f"Received message from {client_address} : {message}")

            # отправляем ответ клиенту
            response = "Hello, client"
            server_socket.sendto(response.encode("utf-8"), client_address)
            print(f"Sent response to {client_address}")
    except Exception:
        print("\nServer shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    run()