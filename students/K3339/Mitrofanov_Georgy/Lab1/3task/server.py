import socket
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8080

INDEX_PATH = Path(__file__).with_name("index.html")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"HTTP server started on http://{HOST}:{PORT}/")

def build_response(body: bytes, status: str = "200 OK", content_type: str = "text/html; charset=utf-8") -> bytes:
    headers = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "",
        ""
    ]
    return ("\r\n".join(headers)).encode("utf-8") + body

while True:
    conn, addr = server_socket.accept()
    try:
        request_data = conn.recv(4096).decode("utf-8", errors="ignore")
        first_line = request_data.splitlines()[0] if request_data else ""
        print(f"Request from {addr}: {first_line}")

        if INDEX_PATH.exists():
            # Читаем HTML и добавляем CSS стили
            html_content = INDEX_PATH.read_text(encoding="utf-8")
            
            # Добавляем стили, если их нет
            if "<style>" not in html_content:
                styled_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Моя страница</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            max-width: 800px;
                            margin: 50px auto;
                            padding: 20px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            border-radius: 10px;
                            box-shadow: 0 0 20px rgba(0,0,0,0.3);
                        }}
                        h1 {{
                            text-align: center;
                            border-bottom: 2px solid white;
                            padding-bottom: 10px;
                        }}
                        p {{
                            line-height: 1.6;
                            font-size: 18px;
                        }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                html = styled_html.encode("utf-8")
            else:
                html = INDEX_PATH.read_bytes()
            
            resp = build_response(html, "200 OK")
        else:
            body = b"""
            <html>
            <head><title>404 Not Found</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: #ff4444;">404</h1>
                <p>index.html not found</p>
                <hr>
                <small>HTTP Server v2.0</small>
            </body>
            </html>
            """
            resp = build_response(body, "404 Not Found")

        conn.sendall(resp)
    finally:
        conn.close()