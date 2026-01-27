import socket
from urllib.parse import parse_qs, unquote_plus
from cfg import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, HTML_FILE

grades = []

def load_html():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def generate_grades_list():
    if not grades:
        return "<p>Оценок пока нет</p>"
    
    items = ""
    for subject, grade in grades:
        items += f"<li><b>{subject}</b> — {grade}</li>"
    
    return f"<ul>{items}</ul>"

def create_response(body):
    body_bytes = body.encode('utf-8')
    
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "\r\n"
    )
    
    return headers.encode('utf-8') + body_bytes

def handle_request(request):
    lines = request.split('\r\n')
    method = lines[0].split(' ')[0]
    print(f"[+] {method} запрос")
    
    if method == 'POST':
        body = request.split('\r\n\r\n')[1]
        params = parse_qs(body)
        
        subject = unquote_plus(params.get('subject', [''])[0])
        grade = params.get('grade', [''])[0]
        
        if subject and grade:
            grades.append((subject, grade))
            print(f"[+] Добавлено: {subject} - {grade}")
    
    html = load_html()
    html = html.replace('{{GRADES_LIST}}', generate_grades_list())
    
    return create_response(html)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    
    print(f"[*] Сервер: http://{SERVER_HOST}:{SERVER_PORT}")
    
    try:
        while True:
            client_socket, _ = server_socket.accept()
            
            request = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            
            if request:
                response = handle_request(request)
                client_socket.send(response)
            
            client_socket.close()
                
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
