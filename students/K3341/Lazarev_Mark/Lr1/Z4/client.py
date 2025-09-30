import socket
import threading
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

def receive_loop(sock):
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("Соединение закрыто сервером.")
                break
            print(data.decode('utf-8'), end='')
    except Exception as e:
        print("Ошибка при приёме:", e)
    finally:
        try:
            sock.close()
        except:
            pass
        sys.exit(0)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))

    # Запускаем поток для получения сообщений от сервера
    threading.Thread(target=receive_loop, args=(sock,), daemon=True).start()

    # Сначала сервер попросит ввести имя — читаем строку и отправляем
    name = input()   # когда подключились, мы увидим "Введите ваше имя: "
    sock.sendall(name.strip().encode('utf-8'))

    # Главный цикл отправки
    try:
        print("Пиши сообщения. Для выхода введи /quit")
        while True:
            line = input()
            if not line:
                continue
            if line.lower() in ('/quit', '/exit'):
                sock.sendall(line.encode('utf-8'))
                break
            sock.sendall(line.encode('utf-8'))
    except KeyboardInterrupt:
        pass
    finally:
        try:
            sock.close()
        except:
            pass
        print("Клиент завершил работу.")

if __name__ == "__main__":
    main()
