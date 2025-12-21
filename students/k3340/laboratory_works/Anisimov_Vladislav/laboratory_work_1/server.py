import socket
import json
import threading
from enum import Enum

class connection_type(Enum):
    UDP = 1
    TCP = 2

class method_type(Enum):
    GET = 1
    POST = 2
    PUT = 3

port = 9090
max_clients = 10
max_data_size = 4 * 1024

class Server:
    clients = {}
    routes = {"GET" : {},
              "PUT" : {},
              "POST" : {}}
    
    def serve_forever(self, host : str, port : int, conn_type : connection_type):
        try:
            self.conn_type = conn_type
            if conn_type == connection_type.UDP:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind((host, port))
                print(f'Server (UDP) is listening at port {port}')
            elif conn_type == connection_type.TCP:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((host, port))
                self.sock.listen(max_clients)
                print(f'Server (TCP) is listening at port {port}')
            self.serve_clients()
        except Exception:
            print(Exception)
        return self

    def serve_clients(self):
        while True:
            if self.conn_type == connection_type.UDP:
                while True:
                    data, client_address = self.sock.recvfrom(max_data_size)
                    if not data:
                        break
                    threading.Thread(target=self.handle_request, args=(data, client_address,)).start()
            elif self.conn_type == connection_type.TCP:
                conn, client_address = self.sock.accept()
                self.clients[client_address] = conn
                print(f"New connection {conn}")
                threading.Thread(target=self.handle_request, args=(conn, client_address,)).start()

    def handle_request(self, conn, client_address):
        if self.conn_type == connection_type.UDP:
            code, message = self.parse_request(conn, client_address)
            self.sock.sendto(bytes(str(self.create_response(code, message)).encode('utf-8')), client_address)
        elif self.conn_type == connection_type.TCP:
            while True:
                try:
                    data = conn.recv(max_data_size)
                    if not data:
                        print("Connection close")
                        conn.close()
                        break
                    code, message = self.parse_request(data, client_address)
                    conn.send(bytes(str(self.create_response(code, message)).encode('utf-8')))
                except:
                    conn.close()

    def parse_request(self, data, client_address):
        out = {}
        out["client_address"] = client_address
        _data = data.decode('utf-8')
        lines = _data.split('\r\n')
        print(f"Recieved data (<= {max_data_size / 1024.0} Kb) from {client_address}: {data.decode('utf-8')}")
        if len(_data) == 0:
            return ""
        method, path, _ = lines[0].split(' ')
        method = method.strip()
        args = ""
        if '?' in path:
            path, args = path.strip().split('?')
        out["path"] = path

        if method == 'POST':
            out["method"] = method_type.POST
            body = str(lines[-1]).strip()
            out["body"] = body
            if body.startswith("{"):
                out["json"] = json.loads(body)
        elif method == 'GET':
            out["method"] = method_type.GET
        if args:
            args_dict = {}
            for arg in args.split("&"):
                key, val = arg.split("=")
                args_dict[key] = val
            out["args"] = args_dict

        if out["method"] not in self.routes or out["path"] not in self.routes[out["method"]]:
            return (404, "Resource not found")

        return self.routes[out["method"]][out["path"]](out)
    
    def create_response(self, code, body):
        length = len(body.encode('utf-8'))
        return f"HTTP/1.1 {code} OK\nContent-Type: application/json,text/html; charset=utf-8\nConnection: keep-alive\nAccess-Control-Allow-Origin: *\nContent-Length: {length}\n\n" + body

    def add_route(self, method : method_type, route : str, handler):
        if method not in self.routes:
            self.routes[method] = {}
        self.routes[method][route] = handler