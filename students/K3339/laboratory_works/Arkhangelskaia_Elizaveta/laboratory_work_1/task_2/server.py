import socket

def pythagoras_theorem_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 8080))
    sock.listen(1)
    print("server is launched, expects a connection...")

    while True:
        connection, client_address = sock.accept()
        print(f"client is connected: {client_address}")

        try:
            data = connection.recv(1024)
            if not data:
                break

            a, b = data.decode().split()
            reply = str((float(a) ** 2 + float(b) ** 2) ** 0.5)
            connection.sendall(reply.encode())
            print(f"answer sent: {reply}")
        except Exception as e:
            print(f"error: {e}")
        finally:
            connection.close()
            print("client turned off")

if __name__ == "__main__":
    pythagoras_theorem_server()
