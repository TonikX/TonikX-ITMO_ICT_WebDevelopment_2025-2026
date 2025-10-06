import socket
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


if __name__ == '__main__':
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))
    print(f"Сервер запущен на {host}:{port}")

    while True:
        data, addr = udp_socket.recvfrom(1024)
        message = data.decode("utf-8")
        print(f"Получено от {addr}: {message}")

        reply = "Hello, client"
        udp_socket.sendto(reply.encode("utf-8"), addr)
