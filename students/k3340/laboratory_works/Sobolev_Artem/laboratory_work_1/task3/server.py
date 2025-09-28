import socket

SERVER_ADDRESS = ("127.0.0.1", 10000)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(SERVER_ADDRESS)
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            try:
                response = conn.recv(1024).decode("utf-8")
                if not response:
                    continue
                headers = response.split('\r\n', 1)[0].split()
                if len(headers) < 3:
                    send_response(conn, create_response(status="HTTP/1.1 400 Bad Request".encode("utf-8")))
                    continue
                method, path, _ = headers
                if method == "GET" and path in ("/index", "/", "/index.html"):
                    send_response(conn, create_response(filepath = "Lab1/task3/" + path))
                elif method != "GET":
                    send_response(conn, create_response(status = b"HTTP/1.1 405 Method Not Allowed"))
                else:
                    send_response(conn, create_response(status = b"HTTP/1.1 404 Not Found"))
            finally:
                conn.close()

def create_response(filepath : str | None = None, status : bytes =b"HTTP/1.1 200 OK") -> bytes:
    body = b""
    if filepath:
        body = read_file(filepath)
    headers = get_headers(body)
    return status + b"\r\n" + headers + b"\r\n" + body

def get_headers(body: bytes) -> bytes:
    return (
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
    ).encode("utf-8")

def read_file(filename : str = "third/index.html") -> bytes:
    with open(filename, "rb") as f:
        body = f.read()
    return body


def send_response(conn, response: bytes):
    conn.sendall(response)

if __name__ == "__main__":
    main()