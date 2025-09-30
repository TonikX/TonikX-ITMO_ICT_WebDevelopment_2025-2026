import socket

SERVER_ADDRESS = "localhost"
SERVER_PORT = 8080
BUF_SIZE = 1024


def quadratic_solver_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("[CLIENT] Enter a, b, c for equation (ax^2 + bx + c = 0) separated by space: ", end="")
        message = input()
        sock.connect((SERVER_ADDRESS, SERVER_PORT))
        sock.sendall(message.encode())
        print("[CLIENT] Waiting for answer...")
        data = sock.recv(BUF_SIZE)
        print(f"[CLIENT] Answer from server: {data.decode()}")
    except Exception as e:
        print(f"[CLIENT] Error: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    quadratic_solver_client()
