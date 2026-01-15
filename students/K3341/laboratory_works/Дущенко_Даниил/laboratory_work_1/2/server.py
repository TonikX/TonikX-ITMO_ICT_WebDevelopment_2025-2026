import socket
import math

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8080))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    data = conn.recv(1024).decode('utf-8')
    if not data:
        conn.close()
        continue
    
    parts = data.split()
    op = parts[0]
    nums = [float(x) for x in parts[1:]]
    result = ""

    if op == '1': 
        res = math.sqrt(nums[0]**2 + nums[1]**2)
        result = f"Hypotenuse: {res}"
    elif op == '2':
        a, b, c = nums[0], nums[1], nums[2]
        d = b**2 - 4*a*c
        if d >= 0:
            x1 = (-b + math.sqrt(d)) / (2*a)
            x2 = (-b - math.sqrt(d)) / (2*a)
            result = f"Roots: {x1}, {x2}"
        else:
            result = "No roots"
    elif op == '3':
        res = (nums[0] + nums[1]) / 2 * nums[2]
        result = f"Trapezoid area: {res}"
    elif op == '4':
        res = nums[0] * nums[1]
        result = f"Parallelogram area: {res}"
    
    conn.send(result.encode('utf-8'))
    conn.close()