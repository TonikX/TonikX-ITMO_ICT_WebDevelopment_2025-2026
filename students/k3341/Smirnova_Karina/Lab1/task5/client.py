import socket

get_request = """GET /marks HTTP/1.1\r
Host: serverName.com\r
Accept: text/html\r
\r
"""

while True:
    print("Выберете запрос:")
    print("1. GET Получить все оценки")
    print("2. POST Создать оценку")
    print("3. Выход")

    command = int(input())

    if command == 1:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 9090))
            client_socket.send(get_request.encode('iso-8859-1'))

            response = client_socket.recv(1024).decode('utf-8')
            print(response, flush=True)

        except Exception as e:
            print("Exception: ", e)

        finally:
            client_socket.close()

    elif command == 2:
        print('Введите предмет и оценку через пробел')
        command = str(input())

        sub, mark = command.split()

        post_request = f"""POST /addMark?sub={sub}&mark={mark} HTTP/1.1\r
Host: serverName.com:9090\r
Content-Length: 0\r
\r
"""

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 9090))
            client_socket.send(post_request.encode('iso-8859-1'))

            response = client_socket.recv(1024).decode('utf-8')
            print(response, flush=True)
        except Exception as e:
            print("Exception: ", e)

        finally:
            client_socket.close()

    elif command == 3:
        break

    else:
        print('Unsupported command')