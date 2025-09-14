#!/usr/bin/env python3
"""
Minimal HTTP server supporting GET and POST using sockets.

Usage:
  python3 task5.py --host 127.0.0.1 --port 8001

The server keeps grades in memory. POST to /add with form fields
`subject` and `grade` to add a record. GET / returns an HTML page
with a form and the list of stored grades.
"""

from __future__ import annotations

import argparse
import socket
import urllib.parse
from typing import Tuple

HOST = '127.0.0.1'
PORT = 8001
BUFFER_SIZE = 8192

# in-memory storage: list of (subject, grade)
grades: list[tuple[str, str]] = []


def build_http_response(body: bytes, status_code: int = 200, content_type: str = 'text/html; charset=utf-8') -> bytes:
    reason = {200: 'OK', 404: 'Not Found', 400: 'Bad Request', 405: 'Method Not Allowed'}.get(status_code, 'OK')
    headers = [
        f'HTTP/1.1 {status_code} {reason}',
        f'Content-Type: {content_type}',
        f'Content-Length: {len(body)}',
        'Connection: close',
        '\r\n'
    ]
    return '\r\n'.join(headers).encode('utf-8') + body


def render_index_page() -> bytes:
    rows = '\n'.join(f"<tr><td>{s}</td><td>{g}</td></tr>" for s, g in grades)
    html = f"""
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>Grades</title></head>
      <body>
        <h1>Grades</h1>
        <form method="post" action="/add">
          <label>Subject: <input name="subject" required></label><br>
          <label>Grade: <input name="grade" required></label><br>
          <button type="submit">Add</button>
        </form>
        <h2>All grades</h2>
        <table border="1">
          <thead><tr><th>Subject</th><th>Grade</th></tr></thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </body>
    </html>
    """
    return html.encode('utf-8')


def parse_headers_and_body(data: bytes) -> tuple[str, dict[str, str], bytes]:
    # returns request_line(str), headers(dict), body(bytes)
    text = data.decode('utf-8', errors='ignore')
    parts = text.split('\r\n\r\n', 1)
    head = parts[0]
    body = parts[1].encode('utf-8') if len(parts) > 1 else b''
    lines = head.split('\r\n')
    request_line = lines[0] if lines else ''
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ':' in line:
            k, v = line.split(':', 1)
            headers[k.strip().lower()] = v.strip()
    return request_line, headers, body


def handle_request(conn: socket.socket, addr: Tuple[str, int]) -> None:
    try:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            return

        request_line, headers, body = parse_headers_and_body(data)
        parts = request_line.split()
        if len(parts) < 3:
            conn.sendall(build_http_response(b'Bad Request', status_code=400, content_type='text/plain'))
            return
        method, path, _ = parts

        if method == 'GET':
            if path == '/' or path.startswith('/'):
                resp = render_index_page()
                conn.sendall(build_http_response(resp, status_code=200, content_type='text/html; charset=utf-8'))
                return
            else:
                conn.sendall(build_http_response(b'Not Found', status_code=404, content_type='text/plain'))
                return

        if method == 'POST':
            # expect POST /add
            if path != '/add':
                conn.sendall(build_http_response(b'Not Found', status_code=404, content_type='text/plain'))
                return

            content_type = headers.get('content-type', '')
            content_length = int(headers.get('content-length', '0') or '0')

            # If body length may be larger than initial recv, try to read remaining
            received_len = len(body)
            while received_len < content_length:
                more = conn.recv(BUFFER_SIZE)
                if not more:
                    break
                body += more
                received_len = len(body)

            # parse form data (application/x-www-form-urlencoded)
            if 'application/x-www-form-urlencoded' in content_type:
                decoded = body.decode('utf-8', errors='ignore')
                params = urllib.parse.parse_qs(decoded)
                subject = params.get('subject', [''])[0].strip()
                grade = params.get('grade', [''])[0].strip()
                print(f"Adding grade: subject={subject}, grade={grade}")
                if subject and grade:
                    grades.append((subject, grade))
                    # after adding, redirect back to /
                    location_body = b''
                    headers_resp = [
                        'HTTP/1.1 303 See Other',
                        'Location: /',
                        'Content-Length: 0',
                        'Connection: close',
                        '\r\n'
                    ]
                    conn.sendall('\r\n'.join(headers_resp).encode('utf-8'))
                    return
                else:
                    conn.sendall(build_http_response(b'Bad Request', status_code=400, content_type='text/plain'))
                    return
            else:
                conn.sendall(build_http_response(b'Unsupported Media Type', status_code=400, content_type='text/plain'))
                return

        # other methods
        conn.sendall(build_http_response(b'Method Not Allowed', status_code=405, content_type='text/plain'))
    except Exception as e: 
        try:
            print(f"Error handling request from {e}.")
            conn.sendall(build_http_response(b'Internal Server Error', status_code=400, content_type='text/plain'))
        except Exception:
            pass


def run_server(host: str = HOST, port: int = PORT) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen(5)
        print(f'Serving on http://{host}:{port}/ (in-memory storage)')
        try:
            while True:
                conn, addr = srv.accept()
                with conn:
                    print(f'Connection from {addr}')
                    handle_request(conn, addr)
        except KeyboardInterrupt:
            print('\nServer stopped')


def parse_args():
    p = argparse.ArgumentParser(description='Minimal HTTP server supporting GET and POST (in-memory grades)')
    p.add_argument('--host', default=HOST)
    p.add_argument('--port', type=int, default=PORT)
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_server(args.host, args.port)
