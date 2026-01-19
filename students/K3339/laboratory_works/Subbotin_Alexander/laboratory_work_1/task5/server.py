import socket 
from urllib.parse import parse_qs

GRADES = {}
HOST = 'localhost'
PORT = 8080
SERV_NAME = 'GradesServer'

class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen(5)
            print(f"Сервер запущен на http://{self._host}:{self._port}")

            while True:
                conn, addr = serv_sock.accept()
                print(f"Подключение от {addr}")
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        except KeyboardInterrupt:
            print("\nСервер остановлен")
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            if req:
                resp = self.handle_request(req)
                self.send_response(conn, resp)
        except ConnectionResetError:
            print("Клиент разорвал соединение")
        except Exception as e:
            print(f"Ошибка: {e}")
            self.send_error(conn, e)
        finally:
            if conn:
                conn.close()

    def parse_request(self, conn):
        """Парсинг HTTP запроса"""
        try:
            request_data = conn.recv(4096).decode('utf-8')
            if not request_data:
                return None

            lines = request_data.split('\r\n')
            request_line = lines[0]
            
            parts = request_line.split(' ')
            if len(parts) != 3:
                return None
                
            method, path, protocol = parts

            headers = {}
            body_start = 0
            for i, line in enumerate(lines[1:], 1):
                if line == '':
                    body_start = i + 1
                    break
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()

            # Извлекаем тело запроса
            body = ''
            if body_start < len(lines):
                body = '\r\n'.join(lines[body_start:])

            return {
                'method': method,
                'path': path,
                'protocol': protocol,
                'headers': headers,
                'body': body
            }
        except Exception as e:
            print(f"Ошибка парсинга запроса: {e}")
            return None

    def handle_request(self, req):
        """Обработка HTTP запроса"""
        method = req['method']
        path = req['path']
        
        print(f"{method} {path}")

        if method == 'GET' and path == '/':
            return self.handle_get_grades()
        elif method == 'POST' and path == '/':
            return self.handle_post_grade(req['body'])
        else:
            return self.handle_404()

    def handle_get_grades(self):
        """Обработка GET запроса - показ формы и оценок"""
        html_content = self.generate_html_page()
        
        return {
            'status': '200 OK',
            'headers': {
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Length': str(len(html_content.encode('utf-8'))),
                'Connection': 'close'
            },
            'body': html_content
        }

    def handle_post_grade(self, body):
        """Обработка POST запроса - добавление оценки"""
        try:
            # Парсим данные формы
            form_data = parse_qs(body)
            subject = form_data.get('subject', [''])[0].strip()
            grade = form_data.get('grade', [''])[0].strip()
            
            if subject and grade:
                # Добавляем оценку
                if subject not in GRADES:
                    GRADES[subject] = []
                GRADES[subject].append(grade)
                print(f"Добавлена оценка: {subject} - {grade}")
            else:
                print("Некорректные данные формы")
            
            # Возвращаем обновленную страницу
            return self.handle_get_grades()
            
        except Exception as e:
            print(f"Ошибка обработки POST: {e}")
            return self.handle_get_grades()

    def handle_404(self):
        """Обработка 404 ошибки"""
        html_content = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>404 - Не найдено</title>
        </head>
        <body>
            <h1>404 - Страница не найдена</h1>
            <p><a href="/">Вернуться на главную</a></p>
        </body>
        </html>
        """
        
        return {
            'status': '404 Not Found',
            'headers': {
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Length': str(len(html_content.encode('utf-8'))),
                'Connection': 'close'
            },
            'body': html_content
        }

    def generate_html_page(self):
        """Генерация HTML страницы"""
        grades_html = ""
        if GRADES:
            grades_html = '<h2>Журнал оценок:</h2><ul class="grades-list">'
            for subject in sorted(GRADES.keys()):
                grades_str = ", ".join(GRADES[subject])
                grades_html += f'''
                    <li class="grade-item">
                        <span class="subject">{subject}</span>
                        <span class="grade">{grades_str}</span>
                    </li>
                '''
            grades_html += '</ul>'
        else:
            grades_html = '<div class="empty-state">Оценок пока нет. Добавьте первую!</div>'

        html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Журнал оценок</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                    margin-bottom: 40px;
                    font-size: 2.5em;
                }}
                .form-section {{
                    background: #f8f9ff;
                    padding: 30px;
                    border-radius: 15px;
                    margin-bottom: 40px;
                    border: 2px solid #e3e8ff;
                }}
                .form-group {{
                    margin-bottom: 25px;
                }}
                label {{
                    display: block;
                    margin-bottom: 8px;
                    font-weight: 600;
                    color: #4a5568;
                    font-size: 1.1em;
                }}
                input[type="text"], select {{
                    width: 100%;
                    padding: 15px;
                    border: 2px solid #e2e8f0;
                    border-radius: 10px;
                    font-size: 16px;
                    transition: all 0.3s ease;
                    box-sizing: border-box;
                }}
                input[type="text"]:focus, select:focus {{
                    border-color: #667eea;
                    outline: none;
                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                }}
                button {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    font-size: 18px;
                    font-weight: 600;
                    width: 100%;
                    transition: transform 0.2s ease;
                }}
                button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
                }}
                .grades-section {{
                    margin-top: 40px;
                }}
                .grades-list {{
                    list-style: none;
                    padding: 0;
                }}
                .grade-item {{
                    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                    margin: 15px 0;
                    padding: 20px;
                    border-radius: 15px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                    transition: transform 0.2s ease;
                }}
                .grade-item:hover {{
                    transform: translateY(-2px);
                }}
                .subject {{
                    font-weight: 600;
                    color: #2d3748;
                    font-size: 1.2em;
                }}
                .grade {{
                    color: #2d3748;
                    font-size: 1.3em;
                    font-weight: 700;
                    background: white;
                    padding: 8px 16px;
                    border-radius: 8px;
                }}
                .empty-state {{
                    text-align: center;
                    color: #718096;
                    font-style: italic;
                    font-size: 1.2em;
                    padding: 60px 20px;
                    background: #f7fafc;
                    border-radius: 15px;
                    border: 2px dashed #cbd5e0;
                }}
                .server-info {{
                    text-align: center;
                    margin-top: 30px;
                    padding: 20px;
                    background: #edf2f7;
                    border-radius: 10px;
                    font-size: 0.9em;
                    color: #4a5568;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Журнал оценок</h1>
                
                <div class="form-section">
                    <h2>Добавить оценку</h2>
                    <form method="POST" action="/">
                        <div class="form-group">
                            <label for="subject">Дисциплина:</label>
                            <input type="text" id="subject" name="subject" required 
                                   placeholder="Введите название дисциплины">
                        </div>
                        
                        <div class="form-group">
                            <label for="grade">Оценка:</label>
                            <select id="grade" name="grade" required>
                                <option value="5">5 Отлично</option>
                                <option value="4">4 Хорошо</option>
                                <option value="3">3 Удовлетворительно</option>
                                <option value="2">2 Неудовлетворительно</option>
                            </select>
                        </div>
                        
                        <button type="submit">Добавить оценку</button>
                    </form>
                </div>
                
                <div class="grades-section">
                    {grades_html}
                </div>
                
                <div class="server-info">
                    Сервер: {self._server_name} | {self._host}:{self._port}
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def send_response(self, conn, resp):
        """Отправка HTTP ответа"""
        try:
            # Формируем HTTP ответ
            response_line = f"HTTP/1.1 {resp['status']}\r\n"
            
            # Добавляем заголовки
            headers = ""
            for key, value in resp['headers'].items():
                headers += f"{key}: {value}\r\n"
            
            # Формируем полный ответ
            full_response = response_line + headers + "\r\n" + resp['body']
            
            # Отправляем
            conn.sendall(full_response.encode('utf-8'))
            print("Ответ отправлен")
            
        except Exception as e:
            print(f"Ошибка отправки ответа: {e}")

    def send_error(self, conn, err):
        """Отправка ошибки"""
        try:
            error_html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Ошибка сервера</title>
            </head>
            <body>
                <h1>500 - Ошибка сервера</h1>
                <p>Произошла ошибка: {str(err)}</p>
                <p><a href="/">Вернуться на главную</a></p>
            </body>
            </html>
            """
            
            response = (
                "HTTP/1.1 500 Internal Server Error\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(error_html.encode('utf-8'))}\r\n"
                "Connection: close\r\n"
                f"\r\n{error_html}"
            )
            
            conn.sendall(response.encode('utf-8'))
            
        except Exception:
            pass


if __name__ == '__main__':
    serv = MyHTTPServer(HOST, PORT, SERV_NAME)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass