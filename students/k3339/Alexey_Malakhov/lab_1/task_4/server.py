import socket
from threading import Thread

history = []
clients = {}


def accept_incoming_connections():
    while True:
        client_connection, client_address = sock.accept()

        print(f'Подключение от {client_address}')
        client_connection.send("Введите ваше имя: ".encode("utf-8"))

        Thread(target=handle_client, args=(client_connection,)).start()


def handle_client(client):
    name = None
    try:
        name = client.recv(1024).decode("utf-8")
        broadcast(f'{name} присоединяется к чату.')

        clients[client] = name

        client.send('\n'.join(history).encode('utf-8'))

        while True:
            msg = client.recv(1024).decode("utf-8")

            if not msg:
                break

            if msg.lower() == 'выход':
                break

            broadcast(msg, name)

    except ConnectionResetError:
        print(f"Клиент {name if name else 'неизвестный'} неожиданно отключился")

    except Exception as e:
        print(f"Ошибка при обработке клиента: {e}")

    finally:
        if client in clients:
            client_name = clients[client]
            broadcast(f'{client_name} покинул чат.')
            del clients[client]

        try:
            client.close()

        except Exception as e:
            print(f"Ошибка сервера: {e}")

        print(f"Клиент {name if name else 'неизвестный'} отключен")


def broadcast(msg, name=''):
    answer = f"{msg}"
    if name:
        answer = f"[{name}]: " + answer
    history.append(answer)
    for client_socket in clients.keys():  # Проходим по сокетам клиентов
        try:
            client_socket.send(answer.encode("utf-8"))
        except Exception as e:
            print(f"Ошибка при отправке сообщения клиенту: {e}")
            client_socket.close()
            del clients[client_socket]


sock = socket.socket()
sock.bind(("", 777))
sock.listen(5)

print("Ждем подключений...")

accept_thread = Thread(target=accept_incoming_connections)
accept_thread.start()
accept_thread.join()

sock.close()
