from MyHTTPServer import MyHTTPServer

if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    serv = MyHTTPServer(host, port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
