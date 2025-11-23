import socket

HOST = '127.0.0.1'
PORT = 8001
ENCODING = 'utf-8'
TIMEOUT = 5.0

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(TIMEOUT)
        s.sendto("Hello, server".encode(ENCODING), (HOST, PORT))
        try:
            data, _ = s.recvfrom(1024)
            print("Сервер:", data.decode(ENCODING))
        except socket.timeout:
            print("Нет ответа")

if __name__ == '__main__':
    main()
