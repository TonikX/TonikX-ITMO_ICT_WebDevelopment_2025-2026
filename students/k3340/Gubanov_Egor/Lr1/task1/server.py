import socket

HOST = '127.0.0.1'
PORT = 8001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP сервер запущен на {HOST}:{PORT}")
        try:
            while True:
                data, addr = s.recvfrom(BUFFER_SIZE)
                if not data:
                    continue
                msg = data.decode(ENCODING)
                print(f"Получено от {addr}: {msg!r}")
                reply = "Hello, client" if msg.strip() == "Hello, server" else f"Server received: {msg}"
                s.sendto(reply.encode(ENCODING), addr)
        except KeyboardInterrupt:
            print("\nСервер завершает работу.")

if __name__ == '__main__':
    main()
