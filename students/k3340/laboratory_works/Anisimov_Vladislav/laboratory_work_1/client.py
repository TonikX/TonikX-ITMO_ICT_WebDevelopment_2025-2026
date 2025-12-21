import socket
import json
import sys

max_data_size = 4 * 1024

def task_1():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("Hello, server!".encode('utf-8'), ('192.168.0.105', 9090))

    data, client_address = sock.recvfrom(max_data_size)
    sock.close()
    print(f"Server answered: {data.decode('utf-8')}")

def task_2():
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send(json.dumps({"op" : 2, "a":10, "b": 50, "c":100}).encode("utf-8"))

    data = sock.recv(max_data_size)
    print(f"Server answered: {data.decode('utf-8')}")
    sock.close()

def task_3():
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send(b"HEAD / HTTP/1.1\r\nHost: 192.168.0.105\r\nAccept: text/html\r\n\r\n")

    data = sock.recv(max_data_size)
    print(f"Server answered: {data.decode('utf-8')}")
    sock.close()

def task_4():
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send(b"POST /join HTTP/1.1\r\nHost: 192.168.0.105\r\nAccept: text/html\r\n\r\n" + json.dumps({"user" : "Vlaani", "chat_id": "First chat"}).encode("utf-8"))
    data = sock.recv(max_data_size)
    print(f"Server answered: {data.decode('utf-8')}")

    sock.send(b"POST /send HTTP/1.1\r\nHost: 192.168.0.105\r\nAccept: text/html\r\n\r\n" + json.dumps({"user" : "Vlaani", "chat_id": "First chat", "text": "Hello everyone!"}).encode("utf-8"))
    data = sock.recv(max_data_size)
    print(f"Server answered: {data.decode('utf-8')}")

    sock.close()

task_3()
