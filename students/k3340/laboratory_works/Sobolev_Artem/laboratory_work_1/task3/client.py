import socket

SERVER_ADDRESS = ("127.0.0.1", 10000)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDRESS)

        request = (
            "GET /index.html HTTP/1.1\r\n"
            "Host: 127.0.0.1:10000\r\n"
            "User-Agent: Mozilla/5.0\r\n"
            "Accept: text/html\r\n"
            "\r\n"
        )

        client_socket.sendall(request.encode("utf-8"))

        data = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            data += chunk

        print(data.decode("utf-8"))

if __name__ == "__main__":
    main()

