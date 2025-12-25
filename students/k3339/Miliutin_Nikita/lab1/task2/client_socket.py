import json
import socket

js_bt = json.dumps(
    {"a": 3, "b": 4}
        ).encode("utf-8")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(("localhost", 9091))

client_socket.connect(("localhost", 9090))
client_socket.send(js_bt)

response = client_socket.recv(1024)
print(f"Площадь трапеции: {response.decode()} см^2")

