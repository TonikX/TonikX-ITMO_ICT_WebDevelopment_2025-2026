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