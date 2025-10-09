# server.py
import socket

HOST = '127.0.0.1'   
PORT = 5000          

def calculate_area(base: float, height: float) -> float:
    """Формула площади параллелограмма: S = a * h"""
    return base * height

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)  
    print(f"TCP server listening on {HOST}:{PORT}...")

    conn, addr = sock.accept()
    print(f"Connected by {addr}")

    with conn:
        
        data = conn.recv(1024).decode('utf-8')
        if not data:
            return

        print(f"Received from client: {data}")
        try:
            base, height = map(float, data.split())  
            area = calculate_area(base, height)
            response = f"Площадь параллелограмма = {area}"
        except Exception as e:
            response = f"Ошибка вычисления: {e}"

        
        conn.sendall(response.encode('utf-8'))
        print(f"Sent to client: {response}")

    sock.close()

if __name__ == '__main__':
    main()
