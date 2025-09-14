#!/usr/bin/env python3
"""
Simple HTTP server

Использование:
  python3 task3.py --host 127.0.0.1 --port 8000

Остальные команды описаны в python task3.py --help
"""

from __future__ import annotations

import argparse
import os
import socket
from typing import Tuple

HOST = '127.0.0.1'
PORT = 8000
BUFFER_SIZE = 4096


def build_http_response(body: bytes, status_code: int = 200, content_type: str = 'text/html; charset=utf-8') -> bytes:
    reason = {200: 'OK', 404: 'Not Found', 400: 'Bad Request'}.get(status_code, 'OK')
    headers = [
        f'HTTP/1.1 {status_code} {reason}',
        f'Content-Type: {content_type}',
        f'Content-Length: {len(body)}',
        'Connection: close',
        '\r\n'
    ]
    return '\r\n'.join(headers).encode() + body


def handle_request(conn: socket.socket, addr: Tuple[str, int], root_dir: str) -> None:
    try:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            return
        text = data.decode(errors='ignore')
        first_line = text.splitlines()[0] if text.splitlines() else ''
        parts = first_line.split()
        if len(parts) < 3:
            resp = build_http_response(b'Bad Request', status_code=400, content_type='text/plain')
            conn.sendall(resp)
            return
        method, path, _ = parts
        if method != 'GET':
            resp = build_http_response(b'Method Not Allowed', status_code=400, content_type='text/plain')
            conn.sendall(resp)
            return

        if path == '/':
            path = '/index.html'
        # prevent path traversal
        safe_path = os.path.normpath(path).lstrip('/')
        full_path = os.path.join(root_dir, safe_path)
        if not os.path.commonpath([os.path.abspath(full_path), os.path.abspath(root_dir)]) == os.path.abspath(root_dir):
            resp = build_http_response(b'Not Found', status_code=404, content_type='text/plain')
            conn.sendall(resp)
            return

        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            resp = build_http_response(b'Not Found', status_code=404, content_type='text/plain')
            conn.sendall(resp)
            return

        with open(full_path, 'rb') as f:
            body = f.read()
        resp = build_http_response(body, status_code=200, content_type='text/html; charset=utf-8')
        conn.sendall(resp)
    except Exception:
        try:
            conn.sendall(build_http_response(b'Bad Request', status_code=400, content_type='text/plain'))
        except Exception:
            pass


def run_server(host: str = HOST, port: int = PORT, root_dir: str | None = None) -> None:
    if root_dir is None:
        root_dir = os.path.dirname(os.path.abspath(__file__))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen(5)
        print(f'Serving HTTP on {host}:{port} (root: {root_dir})')
        try:
            while True:
                conn, addr = srv.accept()
                with conn:
                    print(f'Connection from {addr}')
                    handle_request(conn, addr, root_dir)
        except KeyboardInterrupt:
            print('\nServer stopped by user')


def parse_args():
    p = argparse.ArgumentParser(description='Minimal HTTP server serving index.html using sockets')
    p.add_argument('--host', default=HOST, help=f'Host to bind (default: {HOST})')
    p.add_argument('--port', type=int, default=PORT, help=f'Port (default: {PORT})')
    p.add_argument('--root', default=None, help='Directory to serve files from (default: script directory)')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_server(args.host, args.port, root_dir=args.root)
