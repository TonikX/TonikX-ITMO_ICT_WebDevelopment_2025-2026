import socket

SERVER_ADDRESS = "localhost"
SERVER_PORT = 8080
BUF_SIZE = 1024


def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_ADDRESS, SERVER_PORT))
    print("[SERVER] Started.")

    try:
        while True:
            data, address = sock.recvfrom(BUF_SIZE)
            print(f"[SERVER] Message received from client {address}: {data.decode()}.")
            reply = "Hello, client"
            sock.sendto(reply.encode(), address)
            print(f"[SERVER] Answer {reply} is sent to {address} client.")
    except KeyboardInterrupt:
        print('[SERVER] Stopped.')
    finally:
        sock.close()


if __name__ == "__main__":
    udp_server()
