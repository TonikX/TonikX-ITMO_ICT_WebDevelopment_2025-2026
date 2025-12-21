import math
import cmath
import time
from collections import namedtuple
from urllib.parse import unquote
from server import *

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

def solve_problem(data, client_address):
    problem = json.loads(data)
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

def send_html_page(request):
    file = open("index.html", "r").read()
    return (200, file)

def task_3():
    server = Server()
    server.add_route(method_type.GET, "/", send_html_page)
    server.serve_forever("", port, connection_type.TCP)

class User:
    name : str = ""
    chats : set = set()
    update_event : threading.Event = threading.Event()
    new_messages : dict = {}
    def __init__(self, name):
        self.name = name
        self.chats = set()    
        self.update_event = threading.Event()
        self.new_messages = dict()
            
#User = namedtuple("User", ["name", "chats", "update_event", "event_message", "new_messages"])
Message = namedtuple("Message", ["user", "text", "time"])
Chat = namedtuple("Chat", ["users", "messages"])

server : Server
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
    print(f"User {user.name} joined chat \"{chat_id}\"")
    print(f"Chat {chat_id}: {chats[chat_id].messages}")
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
        print(f"Update set for user {u.name}\n")
    r = args["text"]
    print(f"Got message from user {user.name}: \"{r}\"")
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
                    print(messages_ids)
                    print(chats[id].messages)
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
            
        print(f"Result is {result}")
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
    print("Sended page")
    return (200, file)

def task_4():
    server = Server()
    server.add_route(method_type.POST, "/join", join_route)
    server.add_route(method_type.POST, "/send", send_route)
    server.add_route(method_type.GET, "/login", login_route)
    server.add_route(method_type.GET, "/messages", messages_route)
    server.add_route(method_type.GET, "/", default_route)
    server.add_route(method_type.GET, "/chat.html", default_route)
    server.serve_forever("", port, connection_type.TCP)

grades = {}

def add_route(request):
    body = request["json"]
    global grades
    subject = body["subject"]
    if subject not in grades:
        grades[subject] = []
    grades[subject].append(int(body["grade"]))
    return (200, "Successfully added")

def get_route(request):
    global grades
    return (200, json.dumps(grades))

def get_table_route(request):
    file = open("./table.html", "r").read()
    return (200, file)

def task_5():
    server = Server()
    server.add_route(method_type.POST, "/add", add_route)
    server.add_route(method_type.GET, "/get", get_route)
    server.add_route(method_type.GET, "/", get_table_route)
    server.add_route(method_type.GET, "/chat.html", get_table_route)
    server.serve_forever("", port, connection_type.TCP)

task_5()