import socket
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


if __name__ == '__main__':
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "Hello, server"
    udp_socket.sendto(message.encode("utf-8"), (host, port))

    data, addr = udp_socket.recvfrom(1024)
    print(f"Ответ от сервера: {data.decode('utf-8')}")
