import socket


def run_server():
    try:
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_server.bind(('localhost', 8080))

        print("Сервер запущен и ожидает сообщений...")
        print("Для остановки сервера нажмите Ctrl+C")

        while True:
            try:
                # Получаем данные от клиента
                request, address = sock_server.recvfrom(1024)
                decoded_message = request.decode('utf-8')
                print(f'Client {address}: {decoded_message}')

                # Отправляем ответ клиенту
                response = 'Hello, client'
                sock_server.sendto(response.encode('utf-8'), address)
                print(f"Ответ отправлен клиенту {address}")

            except Exception as e:
                print(f"Ошибка при обработке запроса: {e}")

    except KeyboardInterrupt:
        print("\nСервер остановлен")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        sock_server.close()


if __name__ == "__main__":
    run_server()