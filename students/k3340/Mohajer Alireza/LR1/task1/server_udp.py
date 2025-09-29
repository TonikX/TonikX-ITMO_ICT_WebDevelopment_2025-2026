import socket

HOST = "127.0.0.1"
PORT = 14900
BUFFER_SIZE = 1024

print("SERVER IS RUNNING ...\n")

conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.bind((HOST, PORT))

request, client_address = conn.recvfrom(BUFFER_SIZE)

print(f"NEW CONNECTION FROM: {client_address}\n")

print("\n" + "=" * 80 + "\n")
print("REQUEST FROM CLIENT: \n" + request.decode() + "\n")

conn.sendto("HELLO, CLIENT!".encode(), client_address)

# conn.close()
