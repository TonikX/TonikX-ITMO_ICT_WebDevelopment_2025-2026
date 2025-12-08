import socket

HOST = 'localhost'
PORT = 9091


def run_client():
    # Создаём TCP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Подключаемся к серверу
        client_socket.connect((HOST, PORT))
        print(f"Подключено к серверу {HOST}:{PORT}")

        # Ввод катетов
        a = input("Введите катет a: ")
        b = input("Введите катет b: ")

        # Отправляем данные серверу
        message = f"{a} {b}"
        client_socket.sendall(message.encode('utf-8'))
        print(f"Отправлено на сервер: {message}")

        # Получаем ответ
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Ответ от сервера: {response}")

    except Exception as e:
        print(f"Ошибка клиента: {e}")
    finally:
        client_socket.close()
        print("Клиент завершил работу")


if __name__ == "__main__":
    run_client()
