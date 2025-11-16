# server.py
import socket

HOST = '127.0.0.1'   # адрес для локального теста. Если нужен внешний доступ, используйте '0.0.0.0' или реальный IP.
PORT = 9999          # порт (можно изменить)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP -> SOCK_DGRAM
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    print(f'UDP server listening on {HOST}:{PORT} ...')

    try:
        while True:
            data, addr = sock.recvfrom(1024)  # буфер 1024 байта
            msg = data.decode('utf-8')
            print(f'Received from {addr}: {msg}')

            # Ответ клиенту
            if msg == 'Hello, server':
                reply = 'Hello, client'
            else:
                reply = 'Hello, client (reply)'

            sock.sendto(reply.encode('utf-8'), addr)
            print(f'Sent to {addr}: {reply}\n')
    except KeyboardInterrupt:
        print('\nServer stopped by user')
    finally:
        sock.close()

if __name__ == '__main__':
    main()
