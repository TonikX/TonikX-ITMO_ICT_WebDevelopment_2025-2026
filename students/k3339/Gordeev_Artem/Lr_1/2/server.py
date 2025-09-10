import socket

# AF_INET - IPv4, SOCK_STREAM - TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind(('localhost', 9999))
tcp_socket.listen(5)

while True:
    client_socket, addr = tcp_socket.accept()
    print(f"Получено соединение от {addr}")

    try:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        print(f"Получены данные: '{data}'")

        a_str, b_str = data.split(',')
        a = float(a_str)
        b = float(b_str)

        c = (a ** 2 + b ** 2)**0.5
        result = str(c)
        print(f"Вычислен результат: {result}")

        client_socket.send(result.encode('utf-8'))

    except ValueError:
        error_message = "Ошибка: Неверный формат данных. Ожидались два числа через запятую."
        client_socket.send(error_message.encode('utf-8'))
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        client_socket.close()
        print(f"Соединение с {addr} закрыто")
