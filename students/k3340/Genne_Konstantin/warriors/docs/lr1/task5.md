# Задание
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

**Требования:**

- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.
 
***

# Решение

## Сервер

```python
import socket
import sys
from request import Request
from response import Response
from HTTPError import HTTPError
from email.parser import Parser


MAX_LINE = 64 * 1024
MAX_HEADERS = 100


class MyHTTPServer:
    # Параметры сервера
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name

    def serve_forever(self):
    # 1. Запуск сервера на сокете, обработка входящих соединений
        serv_sock = socket.socket(
           socket.AF_INET,
           socket.SOCK_STREAM,
           proto=0
        )

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            print(f'Сервер запущен на сокете {self._host}:{self._port}')

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                   print('Client serving failed 2', e)
        finally:
           serv_sock.close()

            
    def serve_client(self, conn):
    # 2. Обработка клиентского подключения
        try:
           req = self.parse_request(conn)
           resp = self.handle_request(req)
           self.send_response(conn, resp)
        except ConnectionResetError:
           conn = None
        except Exception as e:
           self.send_error(conn, e)

        if conn:
           req.rfile.close()
           conn.close()


    def parse_request(self, conn):
    # 3. функция для обработки заголовка http+запроса. Python, сокет предоставляет возможность создать вокруг него некоторую обертку, которая предоставляет file object интерфейс. Это дайте возможность построчно обработать запрос. Заголовок всегда - первая строка. Первую строку нужно разбить на 3 элемента  (метод + url + версия протокола). URL необходимо разбить на адрес и параметры (isu.ifmo.ru/pls/apex/f?p=2143 , где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        host = headers.get('Host')
        if not host:
           raise HTTPError(400, 'Bad request', 'Host header is missing')
        if host not in (self._server_name, f'{self._server_name}:{self._port}'):
           raise HTTPError(404, 'not found')
        
        return Request(method, target, ver, headers, rfile)


    def parse_headers(self, rfile):
    # 4. Функция для обработки headers. Необходимо прочитать все заголовки после первой строки до появления пустой строки и сохранить их в массив.
        headers = []
        while True:
           line = rfile.readline(MAX_LINE + 1)
           if len(line) > MAX_LINE:
              raise HTTPError(494, 'Request header too large')
           
           if line in (b'\r\n', b'\n', b''):
              break
           
           headers.append(line)
           if len(headers) > MAX_HEADERS:
              raise HTTPError(494, 'Too many headers')
           
        sheaders = b''.join(headers).decode('iso-8859-1')
           
        return Parser().parsestr(sheaders)


    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise HTTPError(400, 'Bad request', 'Request line is too long')

        req_line = str(raw, 'iso-8859-1')
        req_line = req_line.rstrip('\r\n')
        words = req_line.split()
        if len(words) != 3:
            raise HTTPError(400, 'Bad request', 'Malformed request line')
        
        method, target, version = words
        if version != 'HTTP/1.1':
            raise HTTPError(505, 'HTTP Version Not Supported')
        
        return method, target, version


    def handle_request(self, req):
    # 5. Функция для обработки url в соответствии с нужным методом. В случае данной работы, нужно будет создать набор условий, который обрабатывает GET или POST запрос. GET запрос должен возвращать данные. POST запрос должен записывать данные на основе переданных параметров.
        if req.path == '/addMark' and req.method == 'POST':
           return self.handle_post_marks(req)
        
        if req.path == '/' and req.method == 'GET':
           return self.handle_get_subjects()
        
        if req.path == '/marks' and req.method == 'GET':
            return self.handle_get_marks()

        raise HTTPError(404, 'Not found')


    def send_response(self, conn, resp):
    # 6. Функция для отправки ответа. Необходимо записать в соединение status line вида HTTP/1.1 <status_code> <reason>. Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков.
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
           for (key, value) in resp.headers:
              header_line = f'{key}: {value}\r\n'
              wfile.write(header_line.encode('iso-8859-1'))
        
        wfile.write(b'\r\n')

        if resp.body:
           wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    
    def send_error(self, conn, err):
        try:
          status = err.status
          reason = err.reason
          body = (err.body or err.reason).encode('utf-8')
        except:
           status = 500
           reason = b'Internal Server Error'
           body = b'Internal Server Error'

        resp = Response(status, reason, [('Content-Length', len(body))], body)
        self.send_response(conn, resp)
    

    def handle_get_marks(self):
        contentType = 'text/html; charset=utf-8'

        if all(not lst for lst in subjects.values()):
            marks_html = '''
                <p>Вы еще не добавили ни одной оценки.</p>
            '''
        else:
            marks_html = ''
            for subject, marks in subjects.items():
                marks_list = ', '.join([m for m in marks])
                
                marks_html += f'''
                <div class="subject-group">
                    <h3>{subject}</h3>
                    <p><strong>Оценки:</strong> {marks_list}</p>
                    <p><strong>Количество оценок:</strong> {len(marks)}</p>
                    <hr>
                </div>
                '''
        body = f'''
            <h2>Оценки по всем предметам</h2> 
            {marks_html}
            <div class="navigation">
                <a href="/" class="back-button">Вернуться к проставлению оценок</a>
            </div>
            '''
        
        body = body.encode('utf-8')

        headers = [('Content-Type', contentType),
               ('Content-Length', len(body))]
        
        return Response(200, 'OK', headers, body)


    def handle_post_marks(self, req):
        global subjects
        
        body = req.body
        
        if not body:
            raise HTTPError(400, 'Bad Request', 'No form data received')
        
        sub = body.get('sub')[0]
        mark = body.get('mark')[0]
        
        subjects[sub].append(mark)

        print(f'Пользователь поставил оценку. Дисциплина: {sub}. Оценка: {mark}')

        # Перенаправление на главную страницу
        headers = [('Location', '/')]

        return Response(302, 'Found', headers)


    def handle_get_subjects(self):
        contentType = 'text/html; charset=utf-8'

        subject_options = ''.join(
            f'<option value="{sub}">{sub}</option>' 
            for sub in subjects.keys()
        )
        
        mark_options = ''.join(
            f'<option value="{mark}">{mark}</option>' 
            for mark in MARKS
        )
        
        body = f'''
            <h2>Добавить новую оценку</h2>
            <form action="/addMark" method="POST" enctype="application/x-www-form-urlencoded">
                <label>Предмет: <select name="sub" required>
                    <option value="">-- Выберите --</option>
                    {subject_options}
                </select></label><br>
                
                <label>Оценка: <select name="mark" required>
                    <option value="">-- Выберите --</option>
                    {mark_options}
                </select></label><br>
                
                <button type="submit">Добавить оценку</button>
            </form>

            <div class="navigation">
                <a href="/marks" class="back-button">Посмотреть оценки по всем предметам</a>
            </div>
            '''

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
               ('Content-Length', len(body))]
        
        return Response(200, 'OK', headers, body)


def load_data(file_address):
    try:
        with open(file_address, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_address} не найден!")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла {file_address}: {e}")
        return None


def initialize_data():
    global subjects, MARKS
    
    subjects_data = load_data('Data/subjects.txt')
    if subjects_data is None:
        return False
    elif not subjects_data:
        print("Предупреждение: файл subjects.txt пуст")
        return False
    else:
        subjects = {k: [] for k in subjects_data}
    
    marks_data = load_data('Data/marks.txt')
    if marks_data is None:
        return False
    elif not marks_data:
        print("Предупреждение: файл marks.txt пуст")
        return False
    else:
        MARKS = marks_data
    
    return True
       

if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]
    
    # Инициализируем данные перед созданием сервера
    if not initialize_data():
        print("Ошибка: Не удалось загрузить необходимые файлы. Сервер не запущен.")
        sys.exit(1)

    serv = MyHTTPServer(host, port, name)

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
```

Вспомогательные классы:

request.py
```python
from functools import lru_cache
from urllib.parse import parse_qs, urlparse


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path
    
    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)
    
    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)
    

    @property
    def body(self):
        try:
            size = self.headers.get('Content-Length')
            if not size:
                return {}
        
            content_length = int(size)
            if content_length == 0:
                return {}
            
            raw_body = self.rfile.read(content_length)
            if not raw_body:
                return {}
            
            body_str = raw_body.decode('utf-8')
            return parse_qs(body_str)
        
        except (ValueError, UnicodeDecodeError, Exception) as e:
            print(f"Error parsing request body: {e}")
        return {}
```

response.py
```python
class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body
```

HTTPError.py
```python
class HTTPError(Exception):
    def __init__(self, status, reason, body=None):
        super()
        self.status = status
        self.reason = reason
        self.body = body
```

***

# Пояснение

Сервер реализует простой HTTP/1.1-сервер на сокете. Он обрабатывает GET- и POST-запросы, хранит данные об оценках по предметам в памяти и отображает их через HTML-интерфейс.


**1. Запуск сервера (`serve_forever`)**
Сервер создаёт TCP-сокет, привязывается к `127.0.0.1:9090`.
В бесконечном цикле принимает входящие подключения. Работает только с одним подключением в однопоточном режиме.

**2. Обработка запроса (`serve_client`)**
Для каждого подключения:
  - Парсится HTTP-запрос (`parse_request`);
  - Выполняется логика обработки (`handle_request`);
  - Формируется и отправляется HTTP-ответ (`send_response`).
При ошибках отправляется соответствующий HTTP-статус.

**3. Парсинг HTTP-запроса**
Стартовая строка(`parse_request_line`): извлекаются метод, URL и версия протокола.
Заголовки (`parse_headers`): читаются до пустой строки, проверяются на длину и количество.
Обязательный заголовок `Host` должен совпадать с именем сервера.
URL разбирается с помощью `urlparse` (в классе `Request`), параметры из тела POST-запроса — через `parse_qs`.

**4. Обработка маршрутов (`handle_request`)**
Сервер поддерживает три маршрута:
- `GET /` — отображает форму для добавления оценки (выбор предмета и оценки из заранее загруженных списков).
- `POST /addMark` — добавляет новую оценку в глобальный словарь `subjects` и перенаправляет на главную (`302 Found`).
- `GET /marks` — показывает все сохранённые оценки по предметам.

**5. Отправка ответа (`send_response`)**
Формирует корректный HTTP ответ.

**6. Обработка ошибок (`send_error`)**
При возникновении исключений (в т.ч. `HTTPError`) сервер возвращает соответствующий код ошибки и сообщение.


Данные о **предметах** и **допустимых оценках** загружаются при запуске из файлов `Data/subjects.txt` и `Data/marks.txt`.