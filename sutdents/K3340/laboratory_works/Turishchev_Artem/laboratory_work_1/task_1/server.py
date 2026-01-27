import socket
from config import HOST, PORT


conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.bind((HOST, PORT))
data, addr = conn.recvfrom(1024)
msg = data.decode('utf-8')
print(f"recieved message: {msg}")
if msg == "Hello, server":
    ans_message = "Hello, client"
    conn.sendto(ans_message.encode(), addr)
else:
    print("Unknow message recieved")

conn.close()

