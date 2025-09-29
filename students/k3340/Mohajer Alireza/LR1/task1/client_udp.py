import socket

HOST = "127.0.0.1"
PORT = 14900
BUFFER_SIZE = 1024


conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.connect((HOST, PORT))

print("SENDING A REQUEST TO THE SERVER ...")

conn.send(b"HELLO, SERVER!")

response = conn.recv(BUFFER_SIZE).decode()


print("\n" + "=" * 80 + "\n")
print(f"RESPONSE FROM SERVER:\n{response}\n\n")

# conn.close()
