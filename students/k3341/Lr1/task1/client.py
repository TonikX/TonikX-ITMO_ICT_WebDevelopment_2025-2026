import socket

SERVER_ADDRESS = "localhost"
SERVER_PORT = 8080
BUF_SIZE = 1024


def udp_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        message = "Hello, server"
        print(f"[CLIENT] Sending message '{message}' to {SERVER_ADDRESS}:{SERVER_PORT}")
        sock.sendto(message.encode(), (SERVER_ADDRESS, SERVER_PORT))
        data, _ = sock.recvfrom(BUF_SIZE)
        print(f"[CLIENT] Answer: {data.decode()}")
    finally:
        sock.close()


if __name__ == "__main__":
    udp_client()