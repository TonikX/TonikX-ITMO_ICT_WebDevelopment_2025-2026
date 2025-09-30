# client.py
import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'  # если сервер на твоём компьютере
SERVER_PORT = 5001

def receive_messages(sock: socket.socket):
    """Поток для приёма сообщений от сервера"""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("Соединение разорвано сервером.")
                break
            print(data.decode('utf-8'), end='')  # сервер уже добавляет \n где нужно
        except ConnectionResetError:
            print("Соединение сброшено сервером.")
            break
        except Exception as e:
            print(f"Ошибка при получении: {e}")
            break
    try:
        sock.close()
    except:
        pass
    # Если приём завершился — завершаем программу
    sys.exit(0)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    # Запускаем поток для чтения входящих сообщений
    t = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    t.start()

    try:
        # Сначала ожидаем приглашение ввести имя (сервер это шлёт)
        # Но не обязательно — если сервер не шлёт, мы всё равно просим имя
        # Отправляем имя
        username = input()
        if username.strip():
            sock.sendall(username.strip().encode('utf-8'))
        else:
            sock.sendall("Guest".encode('utf-8'))

        # Теперь ввод сообщений — каждый Enter отправляет сообщение
        while True:
            text = input()
            if not text:
                continue
            if text.lower() in ('/quit', '/exit'):
                sock.sendall(text.encode('utf-8'))
                break
            sock.sendall(text.encode('utf-8'))

    except KeyboardInterrupt:
        print("\nВыход...")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        sys.exit(0)

if __name__ == "__main__":
    print("Введите имя (или нажмите Enter для гостя):")
    main()
