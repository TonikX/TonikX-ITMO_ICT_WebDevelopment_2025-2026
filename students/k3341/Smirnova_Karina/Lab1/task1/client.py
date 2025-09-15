import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    socket.sendto("Hi, server".encode("utf-8"), ('localhost', 9090))

    data, server = socket.recvfrom(1024)
    print(data.decode("utf-8"))

except Exception as e:
    print("Exception: ", e)

finally:
    socket.close()
