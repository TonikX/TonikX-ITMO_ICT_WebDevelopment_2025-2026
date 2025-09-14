#!/usr/bin/env python3
"""
Как использовать (в двух терминалах):

Запустить сервер:
   python3 task1.py --server

В другом терминале запустить клиент:
   python3 task1.py --client

Остальные команды описаны в python task1.py --help
"""

import argparse
import socket
import sys
import time


HOST = '127.0.0.1'
PORT = 9999


def run_server(host: str = HOST, port: int = PORT) -> None:
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
		sock.bind((host, port))
		print(f"Server listening on {host}:{port}")
		try:
			data, addr = sock.recvfrom(1024)
			print(f"Received from {addr}: {data.decode()}")
			reply = "Hello, client"
			sock.sendto(reply.encode(), addr)
			print(f"Sent reply to {addr}: {reply}")
		except KeyboardInterrupt:
			print("Server interrupted by user")


def run_client(host: str = HOST, port: int = PORT, timeout: float = 5.0) -> None:
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
		sock.settimeout(timeout)
		message = "Hello, server"
		try:
			sock.sendto(message.encode(), (host, port))
			print(f"Sent to {host}:{port}: {message}")
			data, addr = sock.recvfrom(1024)
			print(f"Received from {addr}: {data.decode()}")
		except socket.timeout:
			print("No response received (timeout)")
		except Exception as e:
			print(f"Client error: {e}")


def parse_args():
	p = argparse.ArgumentParser(description='UDP client/server demo')
	group = p.add_mutually_exclusive_group(required=True)
	group.add_argument('--server', action='store_true', help='Run as server')
	group.add_argument('--client', action='store_true', help='Run as client')
	p.add_argument('--host', default=HOST, help='Host to bind/connect (default: 127.0.0.1)')
	p.add_argument('--port', type=int, default=PORT, help=f'Port (default: {PORT})')
	return p.parse_args()


if __name__ == '__main__':
	args = parse_args()
	if args.server:
		try:
			run_server(args.host, args.port)
		except Exception as e:
			print(f"Server error: {e}")
			sys.exit(1)
	elif args.client:
		try:
			# small sleep in case server was just started in another process
			time.sleep(0.1)
			run_client(args.host, args.port)
		except Exception as e:
			print(f"Client error: {e}")
			sys.exit(1)

