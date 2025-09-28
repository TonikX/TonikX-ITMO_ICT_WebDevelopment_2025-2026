import socket

SERVER_ADDRESS = ("127.0.0.1", 10000)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

        message = "Hello, server"
        client_socket.sendto(message.encode("utf-8"), SERVER_ADDRESS)

        data, _ = client_socket.recvfrom(1024)
        print(data.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()