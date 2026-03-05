import socket


def get_coefficients():
    while True:
        try:
            a = int(input("Введите коэффициент a: "))
            b = int(input("Введите коэффициент b: "))
            c = int(input("Введите коэффициент c: "))
            return a, b, c
        except ValueError:
            print("Ошибка: Введите целые числа!")


def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))

        print("Решение квадратного уравнения типа ax^2 + bx + c")
        a, b, c = get_coefficients()

        message = f"{a} {b} {c}"
        client_socket.send(message.encode())

        result = client_socket.recv(1024).decode()
        print(f"Результат: {result}")

    except ConnectionRefusedError:
        print("Ошибка: Сервер недоступен.")
    except ConnectionResetError:
        print("Ошибка: Соединение с сервером разорвано.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
