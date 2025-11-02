import socket
import threading
import queue


def handle_user(client_connection, client_address):
    """Обработка клиентского соединения"""
    try:
        nickname = client_connection.recv(1024).decode('utf-8')
        for _, msg in messages:
            client_connection.sendall(('\n' + msg).encode('utf-8'))
    except ConnectionResetError:
        print(f'[INFO]: Разорвал соединение клиент {client_address}')
        return
    except Exception as e:
        print(f'[ERROR]: {e}')
        return

    print(f'[INFO]: Присоединился новый клиент {client_address}')

    message_queue.put((client_connection, f'{nickname} присоединился в чат'))

    while True:
        try:
            msg = client_connection.recv(1024).decode('utf-8')
            if not msg:
                break
            ready_msg = f"{nickname}: {msg}"
            message_queue.put((client_connection, ready_msg))
        except ConnectionResetError:
            print(f'[INFO]: Разорвал соединение клиент {client_address}')
            break
        except Exception as e:
            print(f'[ERROR]: {e}')
            break
    
    message_queue.put((client_connection, f'{nickname} вышел из чата'))


def remove_user(idx: int):
    """Удаление клиента из списка участников чата"""
    clients.pop(idx)


def message_to_chat():
    """Отправка сообщения всем в чате"""
    while True:
        try:
            msg = message_queue.get(timeout=0.1)
            messages.append(msg)
            for idx, client_connection in enumerate(clients):
                try:
                    if client_connection != msg[0]:
                        client_connection.sendall(msg[1].encode('utf-8'))
                except:
                    remove_user(idx)
        except queue.Empty:
            continue


HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print('[INFO]: Сервер запущен')

clients = []

message_queue = queue.Queue()

messages = []

threading.Thread(target=message_to_chat, daemon=True).start()

try:
    while True:
        client_connection, client_address = server_socket.accept()
        clients.append(client_connection)
        threading.Thread(target=handle_user, args=[client_connection, client_address]).start()
except Exception as e:
    print(f'[ERROR]: Ошибка сервера. {e}')