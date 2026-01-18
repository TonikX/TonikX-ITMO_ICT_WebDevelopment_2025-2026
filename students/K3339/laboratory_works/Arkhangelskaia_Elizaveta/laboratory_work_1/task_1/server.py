import socket

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 8080))
    print(f"server is launched")

    try:
        while True:
            data, client_address = sock.recvfrom(1024)
            print(f"message received: {data.decode()}")
            reply = "Hello, client"
            sock.sendto(reply.encode(), client_address)
            print(f"answer is sent")
    except KeyboardInterrupt:
        print('\nserver is stopped')
    finally:
        sock.close()

if __name__ == "__main__":
    udp_server()

