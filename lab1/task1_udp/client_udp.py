import socket


HOST = "localhost"
PORT = 8080


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("localhost", 8080)

    try:
        message = "Hello, server"
        print(f"Sending...")
        sock.sendto(message.encode(), server_address)
        data, _ = sock.recvfrom(1024)
        print(f"Response: {data.decode()}")
    finally:
        sock.close()


if __name__ == "__main__":
    main()