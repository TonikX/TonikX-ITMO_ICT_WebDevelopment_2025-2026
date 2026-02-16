import socket

HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(2.0)

        try:
            msg = "Hello, server!"
            s.sendto(msg.encode('utf-8'), (HOST, PORT))
            print(f"Отправлено сообщение '{msg}' серверу {HOST}:{PORT}")

            data, address = s.recvfrom(BUFFER_SIZE)
            print(f"Получен ответ от {address}: {data.decode('utf-8')}")
        except ConnectionResetError:
            print("Соединение разорвано")
        except TimeoutError:
            print("Нет ответа от сервера")

if __name__ == "__main__":
    main()