from code.config import HOST, PORT
from code.server import MyHTTPServer


if __name__ == '__main__':
    host = HOST  
    port = PORT  
    name = "LABmaker"
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass

