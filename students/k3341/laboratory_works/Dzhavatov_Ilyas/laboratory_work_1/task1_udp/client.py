# client.py
import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
MESSAGE = 'Hello, server'
BUFFER_SIZE = 1024
TIMEOUT = 5.0  # сек

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    try:
        print(f'Sending to {SERVER_HOST}:{SERVER_PORT}: {MESSAGE}')
        sock.sendto(MESSAGE.encode('utf-8'), (SERVER_HOST, SERVER_PORT))

        # ждём ответ от сервера
        data, server_addr = sock.recvfrom(BUFFER_SIZE)
        print(f'Received from server {server_addr}: {data.decode("utf-8")}')
    except socket.timeout:
        print('No response from server (timeout)')
    finally:
        sock.close()

if __name__ == '__main__':
    main()
