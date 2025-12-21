# Отчёт по лабораторной работе №1
Выполнил Анисимов Владислав К3340
## Задание 1
 Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:   
- Обязательно использовать библиотеку socket.   
- Реализовать с помощью протокола UDP.
### Выполнение
Создадим сокет для UDP подключения и отправим ответ клиенту:  
```python
def task_1():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    print(f'Server (udp) is listening at localhost:{port}')

    while True:
        data, client_address = sock.recvfrom(1024)
        if not data:
            break
        print(f"Recieved data (<= 4 Kb): {data.decode('utf-8')}")
        sock.sendto("Hello, client!".encode('utf-8'), client_address)
    socket.close()
```
## Задание 2
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Требования:   
- Обязательно использовать библиотеку socket.   
- Реализовать с помощью протокола TCP.
### Выполнение
Создадим сокет для TCP подключения. Данные посланые клиентом распарсим с помощью json. Затем отправим ответ клиенту:  
```python
def task_2():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(max_clients)
    print(f'Server (tcp) is listening at localhost:{port}')

    while True:
        conn, client_address = sock.accept()
        data = conn.recv(max_data_size)
        if not data:
            print("Connection close")
            conn.close()
            break
        print(f"Recieved data (<= {max_data_size / 1024.0} Kb) from {client_address}: {data.decode('utf-8')}")
        conn.send(bytes(str(solve_problem(data, client_address)).encode('utf-8')))
    socket.close()
```
```python
if problem["op"] == 1:
        return math.sqrt(problem["a"]**2 + problem["b"]**2)
    elif problem["op"] == 2:
        if problem["a"] == 0:
            if problem["b"] == 0:
                if problem["c"] == 0:
                    return "Infinite solutions (0=0)"
                else:
                    return "No solution (c!=0)"
            else:
                # Linear equation bx + c = 0
                return -problem["c"] / problem["b"]
        discriminant = (problem["b"]**2) - (4 * problem["a"] * problem["c"])
        if discriminant > 0:
            root1 = (-problem["b"] - cmath.sqrt(discriminant)) / (2 * problem["a"])
            root2 = (-problem["b"] + cmath.sqrt(discriminant)) / (2 * problem["a"])
            return root1, root2
        elif discriminant == 0:
            root = -problem["b"] / (2 * problem["a"])
            return root
        else:  # discriminant < 0
            root1 = (-problem["b"] - cmath.sqrt(discriminant)) / (2 * problem["a"])
            root2 = (-problem["b"] + cmath.sqrt(discriminant)) / (2 * problem["a"])
            return root1, root2
    elif problem["op"] == 3:
        return (problem["base1"] + problem["base2"]) / 2 * problem["height"]
    elif problem["op"] == 4:
        return problem["base"] * problem["height"]
    
    return "idk..."
```
## Задание 3
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которую сервер подгружает из файла index.html.

Требования:   
- Обязательно использовать библиотеку socket.

### Выполнение
В этом задании используется сервер, который был написан в заданиях 3-5. Здесь создаётся TCP сервер, который просто отсылает страничку в ответ.
```python
def task_3():
    server = Server()
    server.add_route(method_type.GET, "/", send_html_page)
    server.serve_forever("", port, connection_type.TCP)
```
```python
def send_html_page(request):
    file = open("index.html", "r").read()
    return (200, file)
```
## Задание 4
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Требования:   
- Обязательно использовать библиотеку socket.   
- Для многопользовательского чата необходимо использовать библиотеку threading.

### Выполнение
В этом задании используется сервер, который был написан в заданиях 3-5. Здесь создаётся TCP сервер, который обрабатывает пользователей в многопоточном режиме. Код страницы доступен в файле лабораторной. 
```python
def task_4():
    server = Server()
    server.add_route(method_type.POST, "/join", join_route)
    server.add_route(method_type.POST, "/send", send_route)
    server.add_route(method_type.GET, "/login", login_route)
    server.add_route(method_type.GET, "/messages", messages_route)
    server.add_route(method_type.GET, "/", default_route)
    server.add_route(method_type.GET, "/chat.html", default_route)
    server.serve_forever("", port, connection_type.TCP)
```
```python
chats = {}
users = {}
lock = threading.Lock()

def join_route(request):
    args = request["json"]
    userName = args["userName"]
    user = users[userName]
    chat_id = args["chat_id"]
    if chat_id not in chats:
        chats[chat_id] = Chat(set(), list())
    chats[chat_id].users.add(user)
    user.chats.add(chat_id)
    user.update_event.set()
    user.new_messages[chat_id] = [] if len(chats[chat_id].messages) == 0 else [len(chats[chat_id].messages)-1]
    return (200, f"You successfully joined chat \"{chat_id}\"")

def send_route(request):
    global lock
    args = request["json"]
    userName = args["userName"]
    user = users[userName]
    chat_id = args["chat_id"]
    i = 0
    with lock:
        chats[chat_id].messages.append(Message(user.name, args["text"], time.time()))
        i = len(chats[chat_id].messages) - 1
    for u in chats[chat_id].users:
        if chat_id not in u.new_messages: 
            u.new_messages[chat_id] = []
        u.new_messages[chat_id].append(i)
        u.update_event.set()
    r = args["text"]
    return (200, f"You successfully sended a message in chat \"{chat_id}\"")

def login_route(request):
    args = request["args"]
    if "userName" not in args:
        return (422, "")
    userName = unquote(args["userName"])
    if userName not in users:
        user = User(userName)
        users[userName] = user
    return (200, json.dumps("You successfully logged in"))

def messages_route(request):
    args = request["args"]
    result = []
                
    if "userName" not in args:
        return (422, "")
    userName = unquote(args["userName"])
    if userName not in users:
        return (401, "Not logged in")
    else:
        user = users[userName]

    if "chat_id" not in args:
        if "loadAllLast" not in args or args["loadAllLast"] == "false":
            if not user.update_event.is_set():
                user.update_event.wait(timeout=30)
                if not user.update_event.is_set():
                    return (200, json.dumps("no updates"))
            user.update_event.clear()
            for id, messages_ids in user.new_messages.items():
                m_count = len(chats[id].messages)
                if m_count != 0:
                    messages = list(map(lambda x: chats[id].messages[x], messages_ids))
                    result.append((id, messages, str(m_count - len(messages_ids)) + ":" + str(m_count)))
                else:
                    result.append((id, [], "0:0"))
            user.new_messages.clear()
        else:
            user.update_event.clear()
            user.new_messages.clear()
            for index in user.chats:
                m_count = len(chats[index].messages)
                if m_count != 0:
                    result.append((index, [chats[index].messages[-1]], str(m_count - 1) + ":" + str(m_count)))
                else:
                    result.append((index, [], "0:0"))
            
        return (200, json.dumps(result))
    
    cur_chat = unquote(args["chat_id"])
    start = args["range"].split(':')[0]
    end = None
    if (len(args["range"].split(':')) == 2):
        end = args["range"].split(':')[1]
    m = chats[cur_chat].messages
    return (200, json.dumps([(cur_chat, m[int(start):int(end)], args["range"])]))

def default_route(request):
    file = open("./chat.html", "r").read()
    return (200, file)
```
## Задание 5
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

### Выполнение
В этом задании используется сервер, который был написан в заданиях 3-5. Здесь создаётся TCP сервер, который обрабатывает запросы на добавление оценок и выдаёт списки оценок по дисциплинам. Код страницы доступен в файле лабораторной. 
```python
def task_5():
    server = Server()
    server.add_route(method_type.POST, "/add", add_route)
    server.add_route(method_type.GET, "/get", get_route)
    server.add_route(method_type.GET, "/", get_table_route)
    server.add_route(method_type.GET, "/chat.html", get_table_route)
    server.serve_forever("", port, connection_type.TCP)
```
```python
grades = {}

def add_route(request):
    args = request["json"]
    global grades
    subject = args["subject"]
    if subject not in grades:
        grades[subject] = []
    grades[subject].append(int(args["grade"]))
    return (200, "Successfully added")

def get_route(request):
    global grades
    return (200, json.dumps(grades))

def get_table_route(request):
    file = open("./table.html", "r").read()
    return (200, file)
```
Ниже представлен код сервера.
```python
import socket
import json
import threading
from enum import Enum

class connection_type(Enum):
    UDP = 1
    TCP = 2

class method_type(Enum):
    GET = 1
    POST = 2
    PUT = 3

port = 9090
max_clients = 10
max_data_size = 4 * 1024

class Server:
    clients = {}
    routes = {"GET" : {},
              "PUT" : {},
              "POST" : {}}
    
    def serve_forever(self, host : str, port : int, conn_type : connection_type):
        try:
            self.conn_type = conn_type
            if conn_type == connection_type.UDP:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind((host, port))
                print(f'Server (UDP) is listening at port {port}')
            elif conn_type == connection_type.TCP:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((host, port))
                self.sock.listen(max_clients)
                print(f'Server (TCP) is listening at port {port}')
            self.serve_clients()
        except Exception:
            print(Exception)
        return self

    def serve_clients(self):
        while True:
            if self.conn_type == connection_type.UDP:
                while True:
                    data, client_address = self.sock.recvfrom(max_data_size)
                    if not data:
                        break
                    threading.Thread(target=self.handle_request, args=(data, client_address,)).start()
            elif self.conn_type == connection_type.TCP:
                conn, client_address = self.sock.accept()
                self.clients[client_address] = conn
                print(f"New connection {conn}")
                threading.Thread(target=self.handle_request, args=(conn, client_address,)).start()

    def handle_request(self, conn, client_address):
        if self.conn_type == connection_type.UDP:
            code, message = self.parse_request(conn, client_address)
            self.sock.sendto(bytes(str(self.create_response(code, message)).encode('utf-8')), client_address)
        elif self.conn_type == connection_type.TCP:
            while True:
                data = conn.recv(max_data_size)
                if not data:
                    print("Connection close")
                    conn.close()
                    break
                code, message = self.parse_request(data, client_address)
                conn.send(bytes(str(self.create_response(code, message)).encode('utf-8')))

    def parse_request(self, data, client_address):
        out = {}
        out["client_address"] = client_address
        _data = data.decode('utf-8')
        lines = _data.split('\r\n')
        print(f"Recieved data (<= {max_data_size / 1024.0} Kb) from {client_address}: {data.decode('utf-8')}")
        if len(_data) == 0:
            return ""
        method, path, _ = lines[0].split(' ')
        method = method.strip()
        args = ""
        if '?' in path:
            path, args = path.strip().split('?')
        out["path"] = path

        if method == 'POST':
            out["method"] = method_type.POST
            body = str(lines[-1]).strip()
            out["body"] = body
            if body.startswith("{"):
                out["json"] = json.loads(body)
        elif method == 'GET':
            out["method"] = method_type.GET
            if args:
                args_dict = {}
                for arg in args.split("&"):
                    key, val = arg.split("=")
                    args_dict[key] = val
                out["args"] = args_dict

        if out["method"] not in self.routes or out["path"] not in self.routes[out["method"]]:
            return (404, "Resource not found")

        return self.routes[out["method"]][out["path"]](out)
    
    def create_response(self, code, body):
        length = len(body.encode('utf-8'))
        return f"HTTP/1.1 {code} OK\nContent-Type: application/json,text/html; charset=utf-8\nConnection: keep-alive\nAccess-Control-Allow-Origin: *\nContent-Length: {length}\n\n" + body

    def add_route(self, method : method_type, route : str, handler):
        if method not in self.routes:
            self.routes[method] = {}
        self.routes[method][route] = handler
```