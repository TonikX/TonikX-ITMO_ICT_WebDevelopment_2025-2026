import socket
from urllib.parse import parse_qs

HOST = '127.0.0.1'
PORT = 8000
GRADES = {}

def generate_html():
    try:
        with open("index5.html", "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        return "Error: index5.html not found"

    items_html = ""
    for subject in sorted(GRADES):
        grades_str = ", ".join(GRADES[subject])
        items_html += f"<li><b>{subject}</b>: {grades_str}</li>\n"
    
    return html.replace("<paste>", items_html)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server is launched: http://{HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                request = conn.recv(1024).decode('utf-8')
                if not request: continue
                
                try:
                    headers = request.split('\r\n')
                    method = headers[0].split()[0]
                except IndexError:
                    continue

                if method == "POST":
                    try:
                        body = request.split('\r\n\r\n')[1]
                        data = parse_qs(body)
                        subject = data.get('subject', [''])[0].strip()
                        grade = data.get('grade', [''])[0].strip()
                        
                        if subject and grade:
                            if subject not in GRADES:
                                GRADES[subject] = [grade]
                            else:
                                GRADES[subject].append(grade)
                    except IndexError:
                        pass

                response_body = generate_html()
                
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
                    "Connection: close\r\n"
                    "\r\n" +
                    response_body
                )

                conn.sendall(response.encode('utf-8'))

if __name__ == '__main__':
    main()