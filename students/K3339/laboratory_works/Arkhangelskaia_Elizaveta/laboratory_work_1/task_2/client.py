import socket

def pythagoras_theorem_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("localhost", 8080)

    try:
        message = input("Введите два числа через пробел: ")

        sock.sendto(message.encode(), server_address)
        print(f"sending...")
        data, _ = sock.recvfrom(1024)
        print(f"answer: {data.decode()}")
    finally:
        sock.close()

if __name__ == "__main__":
    pythagoras_theorem_client()
