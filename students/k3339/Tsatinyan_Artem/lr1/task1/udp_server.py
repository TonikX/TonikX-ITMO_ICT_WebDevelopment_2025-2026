import socket

HOST = "127.0.0.1" # слушаем локально
PORT = 9999 # любой свободный UDP-порт
BUF_SIZE = 1024
ENC = "utf-8"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock: # socket.AF_INET - ipv4, socket.SOCK_DGRAM - UDP
        sock.bind((HOST, PORT)) # Привязываем сокет к адресу

        # Ожидаем получения сообщения
        while True:
            data, addr = sock.recvfrom(BUF_SIZE)
            msg = data.decode(ENC, errors="replace")
            print(f"Получено от {addr}: {msg}")

            reply = "Hello, client"
            sock.sendto(reply.encode(ENC), addr)

if __name__ == "__main__":
    main()
