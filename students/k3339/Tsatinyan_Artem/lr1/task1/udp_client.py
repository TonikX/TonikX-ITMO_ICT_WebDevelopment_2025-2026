import socket

HOST = "127.0.0.1"
PORT = 9999
BUF_SIZE = 1024
ENC = "utf-8"
TIMEOUT_SEC = 2.0

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Tаймаут ожидания ответа
        sock.settimeout(TIMEOUT_SEC)

        message = "Hello, server"
        sock.sendto(message.encode(ENC), (HOST, PORT))

        try:
            data, addr = sock.recvfrom(BUF_SIZE)
            print(f"Ответ от сервера: {data.decode(ENC)}")
        except socket.timeout:
            print("Сервер не ответил (timeout).")

if __name__ == "__main__":
    main()
