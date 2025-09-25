import socket

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 11111))
        request = (
            "GET / HTTP/1.1\r\n"
            f"Host: 127.0.0.1:11111\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        client_socket.sendall(request.encode("UTF-8"))

        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        print(response.decode("utf-8"))

if __name__ == "__main__":
        run_client()