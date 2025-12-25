import socket
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("localhost", 9090))

server_socket.listen(1)

while True:
    connection_socket, addr = server_socket.accept()
    with connection_socket as conn:
        client_request_data = connection_socket.recv(1024)#.decode("utf-8")
        client_json = json.loads(client_request_data)
        resp_json = {"s": client_json["a"] * client_json["b"]}
        conn.send(json.dumps(resp_json).encode("utf-8"))

