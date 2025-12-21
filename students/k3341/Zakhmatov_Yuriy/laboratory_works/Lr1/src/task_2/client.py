import socket


def run():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    try:
        base = float(input("Введите основание параллелограмма: "))
        height = float(input("Введите высоту параллелограмма: "))

        data = f"{base},{height}"
        client_socket.send(data.encode('utf-8'))

        result = client_socket.recv(1024).decode('utf-8')
        print(f"Площадь параллелограмма: {result}")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    run()