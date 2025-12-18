import socket

# Variables
HOST = "127.0.0.1"
PORT = 8080
BUF_SIZE = 1024

def main():
    # Create UDP connection
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Listen on HOST:PORT
        sock.bind((HOST, PORT))
        print(f"UDP server listens on {HOST}:{PORT}")
        try:
            while True:
                # Receive data on socket
                data, client_address = sock.recvfrom(BUF_SIZE)
                decoded_data = data.decode("utf-8")
                print(f"Request from {client_address}: {decoded_data}")

                reply = "Hello, client".encode("utf-8")
                sock.sendto(reply, client_address)
                print(f"Sent {client_address}: Hello, client")
        except KeyboardInterrupt:
            print("\nShutting down")

if __name__ == "__main__":
    main()