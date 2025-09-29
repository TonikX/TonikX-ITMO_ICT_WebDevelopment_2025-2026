import socket

def pythagoras_theorem_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 8080)

    try:
        sock.connect(server_address)
        message = input("enter two numbers through a gap: ")
        sock.sendall(message.encode())

        print("waiting for answer...")
        data = sock.recv(1024)
        print(f"answer from server: {data.decode()}")
    except Exception as e:
        print(f"error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    pythagoras_theorem_client()
