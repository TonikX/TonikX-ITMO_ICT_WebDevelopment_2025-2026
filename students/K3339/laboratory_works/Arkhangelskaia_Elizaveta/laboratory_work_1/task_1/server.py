import socket

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 8080))
    print(f"server is launched")

    while True:
        data, client_address = sock.recvfrom(1024)
        a, b = data.decode().split(" ")
        reply = str((float(a) ** 2 + float(b)**2)**0.5)
        sock.sendto(reply.encode(), client_address)
        print(f"answer is sent: {reply}")

if __name__ == "__main__":
    udp_server()
