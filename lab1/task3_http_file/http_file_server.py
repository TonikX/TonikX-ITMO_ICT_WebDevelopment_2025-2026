import socket
import os


HOST = "localhost"
PORT = 8088
FILE = "index.html"


def build_response(status, body, content_type="text/html; charset=utf-8"):
    body_bytes = body.encode("utf-8")
    headers = [
        f"HTTP/1.1 {status}",
        "Server: SimpleSocketHTTP",
        f"Content-Length: {len(body_bytes)}",
        f"Content-Type: {content_type}",
        "Connection: close",
        "",
        ""
    ]
    return ("\r\n".join(headers)).encode("utf-8") + body_bytes

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[HTTP SERVER] {HOST}:{PORT} - serving {FILE}")
        while True:
            conn, addr = s.accept()
            with conn:
                request = conn.recv(4096)

                try:
                    request_line = request.split(b"\r\n", 1)[0].decode("utf-8", errors="replace")
                except Exception:
                    request_line = ""
                if request_line.startswith("GET "):
                    if os.path.exists(FILE):
                        with open(FILE, "r", encoding="utf-8") as f:
                            body = f.read()
                        resp = build_response("200 OK", body)
                    else:
                        resp = build_response("404 Not Found ", "<h1>404 Not Found</h1>")
                else:
                    resp = build_response("405 Method Not Allowed", "<h1>405 Method Not Allowed</h1>")
                conn.sendall(resp)

if __name__ == "__main__":
    main()
