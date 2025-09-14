#!/usr/bin/env python3
"""
Multi-user chat supporting TCP and UDP

Использование
  TCP server: python3 task4.py --mode server --host 127.0.0.1 --port 12000
  TCP client: python3 task4.py --mode client --host 127.0.0.1 --port 12000 --name Alice

Остальные команды описаны в python3 task4.py --help
"""

from __future__ import annotations

import argparse
import socket
import threading
from typing import Dict, Tuple

BUFFER_SIZE = 4096


def tcp_server(host: str, port: int) -> None:
    clients: Dict[threading.Thread, socket.socket] = {}
    clients_lock = threading.Lock()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen()
    print(f"TCP server listening on {host}:{port}")

    def broadcast(message: bytes, exclude: socket.socket | None = None) -> None:
        with clients_lock:
            for sock in list(clients.values()):
                try:
                    if sock is exclude:
                        continue
                    sock.sendall(message)
                except Exception:
                    pass

    def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
        print(f"Client connected: {addr}")
        try:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                # broadcast received message to other clients
                broadcast(data, exclude=conn)
        except Exception as e:
            print(f"Error with client {addr}: {e}")
        finally:
            with clients_lock:
                # remove this connection from clients
                for t, s in list(clients.items()):
                    if s is conn:
                        del clients[t]
                        break
            try:
                conn.close()
            except Exception:
                pass
            print(f"Client disconnected: {addr}")

    try:
        while True:
            conn, addr = srv.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            with clients_lock:
                clients[t] = conn
            t.start()
    except KeyboardInterrupt:
        print("\nTCP server stopped")
    finally:
        srv.close()


def tcp_client(host: str, port: int, name: str | None = None) -> None:
    if not name:
        name = 'Anonymous'

    def recv_loop(sock: socket.socket) -> None:
        try:
            while True:
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    print('Disconnected from server')
                    break
                print(data.decode(errors='ignore'))
        except Exception:
            pass

    try:
        with socket.create_connection((host, port)) as s:
            print(f"Connected to TCP server at {host}:{port}")
            rthread = threading.Thread(target=recv_loop, args=(s,), daemon=True)
            rthread.start()
            # send loop
            while True:
                line = input()
                if not line:
                    continue
                if line.strip().lower() == '/quit':
                    break
                msg = f"{name}: {line}\n".encode()
                try:
                    s.sendall(msg)
                except Exception:
                    print('Failed to send, exiting')
                    break
    except KeyboardInterrupt:
        print('\nClient stopped')
    except Exception as e:
        print(f"Client error: {e}")



def parse_args():
    p = argparse.ArgumentParser(description='Multi-user chat (TCP/UDP) using sockets and threading')
    p.add_argument('--mode', choices=['server', 'client'], required=True, help='Run as server or client')
    p.add_argument('--host', default='127.0.0.1', help='Host to bind/connect (default: 127.0.0.1)')
    p.add_argument('--port', type=int, required=True, help='Port to bind/connect')
    p.add_argument('--name', help='Client name (for clients)')
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode == 'server':
        tcp_server(args.host, args.port)
    elif args.mode == 'client':
        tcp_client(args.host, args.port, name=args.name)


if __name__ == '__main__':
    main()
