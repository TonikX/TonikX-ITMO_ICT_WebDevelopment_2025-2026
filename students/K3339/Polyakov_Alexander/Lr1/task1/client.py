import socket
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUF_SIZE = 1024
TIMEOUT_SEC = 3

def main():
    # Define server
    server = (SERVER_HOST, SERVER_PORT)

    # Create socker
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT_SEC)

        message = "Hello, server".encode("utf-8")
        sock.sendto(message, server)
        print("Sent to server: Hello, server")

        data, server_address = sock.recvfrom(BUF_SIZE)
        print(f"Response from {server_address}: {data.decode('utf-8')}")

if __name__ == "__main__":
    main()
