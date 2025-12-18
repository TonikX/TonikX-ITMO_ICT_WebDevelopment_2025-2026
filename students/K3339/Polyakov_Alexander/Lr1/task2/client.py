import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
ENC = "utf-8"

def recv_until(sock: socket.socket, delim: bytes = b"\n", bufsize: int = 1024) -> bytes:
    data = bytearray()
    while True:
        chunk = sock.recv(bufsize)
        if not chunk:
            break
        data += chunk
        if delim in chunk:
            break
    return bytes(data)

def main():
    print("Solving a*x^2 + b*x + c = 0")
    a = input("a = ").strip()
    b = input("b = ").strip()
    c = input("c = ").strip()

    # Encode message to send it with socket
    encoded_data = f"{a} {b} {c}\n".encode(ENC)

    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        # Send encoded data to server
        sock.sendall(encoded_data)
        resp = recv_until(sock, b"\n")
        if not resp:
            print("Empte response.")
            return
        print(resp.decode(ENC).strip())

if __name__ == "__main__":
    main()
