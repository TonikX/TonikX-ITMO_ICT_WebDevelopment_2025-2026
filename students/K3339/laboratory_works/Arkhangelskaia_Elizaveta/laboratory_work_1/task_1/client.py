import socket

def udp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("localhost", 8080)

    try:
        message = "Hello, server"
        print(f"sending...")
        sock.sendto(message.encode(), server_address)
        data, _ = sock.recvfrom(1024)
        print(f"answer: {data.decode()}")
    finally:
        sock.close()

if __name__ == "__main__":
    udp_client()
