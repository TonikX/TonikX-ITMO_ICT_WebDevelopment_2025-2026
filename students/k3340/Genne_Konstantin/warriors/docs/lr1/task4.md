# Задание
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте 
многопользовательский чат.

**Требования:**

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.
- Протокол TCP: 100% баллов.
- Протокол UDP: 80% баллов.
- Для UDP используйте threading для получения сообщений на клиенте.
- Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять
пользователей, чтобы отправлять им сообщения.
 
***

# Решение

## Клиент

```python
import threading
import sys
import msvcrt
import queue
import os
import socket


def receive_messages():
    """Получение сообщений от сервера"""
    while running.is_set():
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                print('\nСервер разорвал соединение')
                break
            message_queue.put(msg)
        except ConnectionAbortedError:
            break
        except Exception as e:
            print(f'\nОшибка: {e}', flush=True)
            break
    close_connection()
            
            
def send_message(msg: str):
    client_socket.sendall(msg.encode('utf-8'))


def close_connection():
    running.clear()
    client_socket.close()


def draw_screen():
    """Перерисовывает весь экран: чистый фон + все сообщения + текущий ввод"""
    os.system('cls')

    print("Для выхода из чата набери \\q \n")

    for msg in messages:
        print(msg)

    print(f"\nТы: {user_input}", end="", flush=True)

    cursor_pos = len("Ты: ") + len(user_input) + 1
    sys.stdout.write(f"\033[{cursor_pos}G")
    sys.stdout.flush()


def read_input():
    """Неблокирующее чтение клавиш с поддержкой Unicode"""
    global user_input
    while running.is_set():
        if msvcrt.kbhit():
            char = msvcrt.getwch()
            if char == '\r':
                if user_input == '/q':
                    close_connection()
                    break
                elif user_input.strip():
                    messages.append(f"Ты: {user_input}")
                    send_message(user_input)
                user_input = ""
                draw_screen()
            elif char == '\x08':
                if user_input:
                    user_input = user_input[:-1]
                    draw_screen()
            elif ord(char) == 224:  # Специальные клавиши
                msvcrt.getwch()
            else:
                if char.isprintable():
                    user_input += char
                    draw_screen()


def update_messages():
    """Обновляет историю при новых сообщениях"""
    while running.is_set():
        try:
            msg = message_queue.get(timeout=0.1)
            messages.append(msg)
            draw_screen()
        except queue.Empty:
            continue


HOST = '127.0.0.1'
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))

    nickname = input('Введите свой никнейм: ')

    send_message(nickname)

    message_queue = queue.Queue()
    user_input = ""  # Текущий ввод пользователя
    messages = []    # История сообщений
    running = threading.Event()
    running.set()

    threading.Thread(target=update_messages, daemon=True).start()
    threading.Thread(target=receive_messages, daemon=True).start()

    read_input()

except Exception as e:
    print(f'Ошибка соединения: {e}')
```

## Сервер

```python
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
```

***

# Пояснение

Создаём TCP сокет на сервере, используя адрес `127.0.0.1` и порт `9090`, и ожидаем подключений.
При подключении нового клиента запускается отдельный поток (`handle_user`), в котором:  

- Принимается никнейм пользователя.
- Новому клиенту отправляется история сообщений чата.
- Все последующие сообщения от клиента помещаются в общую очередь `message_queue`.  

Отдельный фоновый поток (`message_to_chat`) постоянно проверяет очередь и рассылает новые сообщения всем подключённым клиентам, кроме отправителя.
При отключении клиента сервер уведомляет остальных участников чата.


Создаём TCP порт на клиенте и подключаемся к серверу на `127.0.0.1:9090`.
После ввода никнейма запускаются три потока:  
  1. `receive_messages` — получает сообщения от сервера и помещает их в локальную очередь.  
  2. `update_messages` — извлекает сообщения из очереди и добавляет в историю чата.  
  3. `read_input` — обрабатывает ввод пользователя.  
Интерфейс чата перерисовывается после каждого действия (`draw_screen`), таким образом обеспечивается одновременный ввод сообщения пользователем и получение сообщений от других участников чата.
Для выхода из чата пользователь вводит `/q`, после чего соединение закрывается.


Как на сервере, так и на клиенте обмен данными между потоками организован через очереди (`queue.Queue`) для потокобезопасности.