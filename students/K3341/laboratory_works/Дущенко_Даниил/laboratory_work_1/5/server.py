import socket
from urllib.parse import unquote_plus

grades = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8080))
sock.listen(5)
print("Сервер запущен: http://127.0.0.1:8080")

while True:
    try:
        conn, addr = sock.accept()
        req = conn.recv(8192).decode('utf-8')
        
        if not req: 
            conn.close()
            continue
        
        if 'POST' in req.split('\n')[0]:
            body = req.split('\r\n\r\n')[1]
            params = {}
            for p in body.split('&'):
                if '=' in p:
                    key, val = p.split('=')
                    params[key] = unquote_plus(val)
            
            if 'subj' in params and 'grade' in params:
                grades.append(params)
        if not grades:
            html_rows = "<tr><td colspan='2' style='text-align:center; color: #777;'>Пока нет записей</td></tr>"
        else:
            html_rows = "".join([f"<tr><td>{g['subj']}</td><td>{g['grade']}</td></tr>" for g in grades])
        
        page = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="utf-8">
            <title>Журнал оценок</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f7f6;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                }}
                .card {{
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                    width: 400px;
                }}
                h2 {{
                    text-align: center;
                    color: #333;
                    margin-bottom: 25px;
                    font-weight: 600;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 25px;
                    font-size: 14px;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                    text-align: left;
                    padding: 12px;
                    border-radius: 4px 4px 0 0;
                }}
                td {{
                    padding: 12px;
                    border-bottom: 1px solid #eee;
                    color: #555;
                }}
                tr:last-child td {{
                    border-bottom: none;
                }}
                form {{
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }}
                input[type="text"] {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    outline: none;
                    transition: border 0.3s;
                }}
                input[type="text"]:focus {{
                    border-color: #4CAF50;
                }}
                input[type="submit"] {{
                    padding: 12px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: background 0.3s;
                }}
                input[type="submit"]:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>📚 Учет успеваемости</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Дисциплина</th>
                            <th>Оценка</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_rows}
                    </tbody>
                </table>
                
                <form method="POST">
                    <input type="text" name="subj" placeholder="Название предмета" required>
                    <input type="text" name="grade" placeholder="Оценка" required>
                    <input type="submit" value="Добавить запись">
                </form>
            </div>
        </body>
        </html>
        """
        
        resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + page
        conn.sendall(resp.encode('utf-8'))
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        conn.close()