import socket
import json

HOST = '127.0.0.1'
PORT = 8002
ENCODING = 'utf-8'

def main():
    print("Решение квадратного уравнения ax² + bx + c = 0")
    params = input("Введите коэффициенты a b c через пробел: ").split()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall((json.dumps({"params": params}) + "\n").encode(ENCODING))
        response = ""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data.decode(ENCODING)
            if "\n" in response:
                break
        
        resp = json.loads(response.strip())
        if resp.get("status") == "ok":
            print("Результат:", resp["result"])
        else:
            print("Ошибка:", resp.get("error"))

if __name__ == '__main__':
    main()
