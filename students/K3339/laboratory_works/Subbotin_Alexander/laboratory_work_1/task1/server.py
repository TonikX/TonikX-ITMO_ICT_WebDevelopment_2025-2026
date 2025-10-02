import socket

HOST = 'localhost'
PORT = 8080

def udp_server():
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.bind((HOST, PORT))

    print(f"Сервер запущен на порту: {PORT}")

    while True:
        data, client_addr = conn.recvfrom(1024)
        print(f'Подключение от {client_addr}')

        request = data.decode("utf-8")
        print(f"Запрос с клиентской стороны: {request}")

        response = "Hello, client"
        conn.sendto(response.encode(), client_addr)

if __name__ == "__main__":
    udp_server()
