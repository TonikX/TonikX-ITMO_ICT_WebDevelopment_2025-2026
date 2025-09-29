import socket
import os

HOST = "127.0.0.1"
PORT = 8080
INDEX = "index.html"

def build_response(status, body):
    body_bytes = body if isinstance(body, bytes) else body.encode("utf-8")
    headers = f"HTTP/1.1 {status}\r\nContent-Length: {len(body_bytes)}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    return headers.encode("utf-8") + body_bytes

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[HTTP SERVER] http://{HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            with conn:
                conn.recv(1024)
                if os.path.exists(INDEX):
                    with open(INDEX, "rb") as f:
                        body = f.read()
                    resp = build_response("200 OK", body)
                else:
                    resp = build_response("404 Not Found", "<h1>404</h1>")
                conn.sendall(resp)

if __name__ == "__main__":
    main()
