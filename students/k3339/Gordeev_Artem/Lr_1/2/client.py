import socket

# AF_INET - IPv4, SOCK_STREAM - TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('localhost', 9999)

try:
    tcp_socket.connect(addr)
    print(f"Успешно подключено")

    a = input("Введите длину первого катета (a): ")
    b = input("Введите длину второго катета (b): ")

    message = f"{a},{b}"
    tcp_socket.send(message.encode('utf-8'))

    result = tcp_socket.recv(1024).decode('utf-8')
    print(f"Результат от сервера: {result}")


except ConnectionRefusedError:
    print("Не удалось подключиться")
except ValueError:
    print("Ошибка ввода")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    tcp_socket.close()
    print("Соединение закрыто")