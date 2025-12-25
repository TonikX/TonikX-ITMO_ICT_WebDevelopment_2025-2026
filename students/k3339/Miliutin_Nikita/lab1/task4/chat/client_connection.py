from __future__ import annotations
import socket
import json
import threading
from chat.server_messages import DISCONECT, GIVE_NAME, HELLOW_TO_NEW
from chat.config import BUFFER_SIZE, ENCODING
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from chat.server import Server

class ClientConnection:
    
    def __init__(self, connection: socket.socket, address: tuple, server: "Server") -> None:
        self.conn = connection
        self.addr = address
        self.name = ""
        self.serv = server
        self.l_thread = threading.Thread(target=self.listen, daemon=True)
        self.l_thread.start()
        

    def send(self, mess: str) -> None:
        self.conn.send(mess.encode(ENCODING))

    
    def send_json(self, mess: dict):
        self.conn.send(json.dumps(mess).encode(ENCODING))


    def listen(self) -> None:
        self.set_name()
        while True:
            try:
                data = self.conn.recv(BUFFER_SIZE).decode(ENCODING)
                print(f"Принял сообщение:{data}")
                if not data:
                    break
                self.serv.broadcast_mes(self.name +": "+ data)
            except Exception as e:
                print(e)
                break
        self.serv.remove_client(self)
        self.serv.broadcast_mes(DISCONECT + self.name)
        self.conn.close()
        print(f"Закрываю соединение с {self.name}")
    

    def set_name(self) -> None:
        try:
            self.send_json(GIVE_NAME)
            data = json.loads(self.conn.recv(BUFFER_SIZE).decode(ENCODING))
            print("Принял сообщение об имени: " + str(data))
            if not isinstance(data, dict):
                raise Exception
            else:
                self.name = data["name"]
                self.serv.broadcast_mes(HELLOW_TO_NEW + self.name)
        except Exception as e:
            self.conn.close()
            print(e)

