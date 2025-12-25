import socket
import threading
from chat.client_connection import ClientConnection
from chat.config import BACKLOG, HOST, PORT
from chat.server_messages import CHAT_INIT

class Server:

    def __init__(self) -> None:
        self.c_conns = []
        self.history = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(BACKLOG)
        self.lock = threading.Lock()
        self.broadcast_mes(CHAT_INIT)
        self.connection_accept()
    
    def connection_accept(self) -> None:
        while True:
            conn, addr = self.server_socket.accept()
            cc = ClientConnection(conn, addr, self)
            with self.lock:    
                self.c_conns.append(cc)

        
    def broadcast_mes(self, mes: str) -> None:
        with self.lock:
            copy_conns = self.c_conns[:]
        dead = []
        
        for cc in copy_conns:
            try:
                cc.send(mes)
            except:
                dead.append(cc)
            self.add_tohistory(mes)
        with self.lock:
            for cc in dead:
                 if cc in self.c_conns:
                     self.c_conns.remove(cc)


    def add_tohistory(self, mes: str):
        with self.lock:
            self.history.append(mes)
    

    def remove_client(self, cc: ClientConnection):
        with self.lock:
            if cc in self.c_conns:
                self.c_conns.remove(cc)
