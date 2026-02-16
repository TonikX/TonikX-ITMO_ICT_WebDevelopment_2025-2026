import socket

HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))    
        print(f"UDP сервер запущен на {HOST}:{PORT}")

        try:
            while True:
                data, client_addr = s.recvfrom(BUFFER_SIZE)
                print(f"Получены данные от {client_addr}: {data.decode('utf-8')}")
                reply = "Hello, client!"
                s.sendto(reply.encode('utf-8'), client_addr)
                print(f"Отправлено сообщение '{reply}' клиенту {client_addr}")
        except KeyboardInterrupt:
            print("UDP сервер остановлен")

if __name__ == "__main__":
    main()