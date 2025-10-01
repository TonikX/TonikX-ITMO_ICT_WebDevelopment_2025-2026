# Lab 1 / Task 4 — Chat Server and Client

This task implements a **multi-user chat** using Python sockets and threads.

## Files
- `server.py` — handles multiple clients, message broadcasting.
- `client.py` — connects to the server and sends/receives messages.

---

## Server (`server.py`)

```python
import threading
import socket

class Server:
    def __init__(self):
        self.clients = {}
        self.server_socket = None
        self.host = 'localhost'
        self.port = 8080

    def listen(self):
        ...
```

## Client (`client.py`)

```python
import threading
import socket

class Client:
    def __init__(self, name):
        self.name = name
        self.host = 'localhost'
        self.port = 8080
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_chat(self):
        ...
```
