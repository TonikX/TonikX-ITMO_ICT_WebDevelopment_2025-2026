#!/usr/bin/env python3
"""
Как использовать (в двух терминалах):

Запустить сервер:
   python3 task2.py --server

В другом терминале запустить клиент:
   python3 task2.py --client

Остальные команды описаны в python task2.py --help
"""

from __future__ import annotations

import argparse
import math
import socket
from typing import Tuple

HOST = '127.0.0.1'
PORT = 10000
BUFFER_SIZE = 1024


def parse_pair(s: str) -> Tuple[float, float]:
    s = s.strip()
    if not s:
        raise ValueError("empty input")
    for sep in (',', None):
        try:
            parts = s.split(sep) if sep is not None else s.split()
            if len(parts) != 2:
                continue
            a, b = float(parts[0]), float(parts[1])
            return a, b
        except Exception:
            continue
    raise ValueError(f"could not parse two numbers from: '{s}'")


def run_server(host: str = HOST, port: int = PORT) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen()
        print(f"Server listening on {host}:{port}")
        try:
            while True:
                conn, addr = srv.accept()
                with conn:
                    print(f"Connection from {addr}")
                    data = b""
                    try:
                        data = conn.recv(BUFFER_SIZE)
                        if not data:
                            print("No data received, closing connection")
                            continue
                        line = data.decode().strip()
                        print(f"Received: {line}")
                        try:
                            a, b = parse_pair(line)
                            hyp = math.hypot(a, b)
                            resp = f"{hyp}\n"
                        except ValueError as e:
                            resp = f"ERROR: {e}\n"
                        conn.sendall(resp.encode())
                        print(f"Sent: {resp.strip()}")
                    except Exception as e:
                        print(f"Error handling client {addr}: {e}")
        except KeyboardInterrupt:
            print("Server interrupted by user, exiting")


def run_client(host: str = HOST, port: int = PORT, timeout: float = 5.0) -> None:
    print("Enter two lengths for a right triangle.")
    try:
        a_str = input("First lengths (a): ").strip()
        b_str = input("Second lengths (b): ").strip()
        try:
            a, b = parse_pair(f"{a_str} {b_str}")
        except ValueError:
            try:
                a, b = parse_pair(a_str)
            except ValueError:
                raise
    except Exception as e:
        print(f"Input error: {e}")
        return

    msg = f"{a} {b}\n"
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.sendall(msg.encode())
            print(f"Sent to {host}:{port}: {a} {b}")
            data = s.recv(BUFFER_SIZE)
            if not data:
                print("No response from server")
                return
            resp = data.decode().strip()
            if resp.startswith("ERROR:"):
                print(f"Server error: {resp}")
            else:
                try:
                    val = float(resp)
                    print(f"Hypotenuse: {val}")
                except Exception:
                    print(f"Unexpected server reply: {resp}")
    except Exception as e:
        print(f"Client error: {e}")


def parse_args():
    p = argparse.ArgumentParser(description='TCP client/server for Pythagoras theorem')
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--server', action='store_true', help='Run as server')
    group.add_argument('--client', action='store_true', help='Run as client')
    p.add_argument('--host', default=HOST, help=f'Host (default: {HOST})')
    p.add_argument('--port', type=int, default=PORT, help=f'Port (default: {PORT})')
    p.add_argument('--timeout', type=float, default=5.0, help='Client timeout in seconds')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.server:
        try:
            run_server(args.host, args.port)
        except Exception as e:
            print(f"Server error: {e}")
            exit(1)
    elif args.client:
        try:
            run_client(args.host, args.port, timeout=args.timeout)
        except Exception as e:
            print(f"Client error: {e}")
            exit(1)
