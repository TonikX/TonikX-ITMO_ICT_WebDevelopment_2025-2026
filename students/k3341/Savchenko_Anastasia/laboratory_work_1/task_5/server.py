import socket
from urllib.parse import parse_qs, unquote


# unquote - для декодирования URL-параметров (например, пробелы кодируются как %20)
# parse_qs - для парсинга параметров вида ключ=значение&ключ2=значение2

class MyHTTPServer:
    # Параметры сервера
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._grades = {}  # Хранилище оценок: {дисциплина: [оценки]}

    def serve_forever(self):
        # 1. Запуск сервера на сокете, обработка входящих соединений
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.bind((self._host, self._port))
        serv_sock.listen()
        serv_sock.settimeout(1)  # Для обработки KeyboardInterrupt Ctrl+C для остановки

        print(f"Сервер запущен на http://{self._host}:{self._port}")

        try:
            while True:
                try:
                    conn, _ = serv_sock.accept()
                    self.serve_client(conn)
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nСервер остановлен")
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        # 2. Обработка клиентского подключения
        try:
            req = self.parse_request(conn)  # разбирает HTTP-запрос (получаем метод, URL, заголовки, тело)
            if req:
                resp = self.handle_request(req)  # обрабатывает запрос в зависимости от метода и пути
                self.send_response(conn, resp)
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            conn.close()

    def parse_request(self, conn):
        # 3. функция для обработки заголовка http+запроса.
        # Python, сокет предоставляет возможность создать вокруг него некоторую обертку, которая предоставляет file object интерфейс.
        # Это дайте возможность построчно обработать запрос. Заголовок всегда - первая строка.
        # Первую строку нужно разбить на 3 элемента  (метод + url + версия протокола).
        # URL необходимо разбить на адрес и параметры (isu.ifmo.ru/pls/apex/f?p=2143 , где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)
        try:
            rfile = conn.makefile('rb')

            # Читаем первую строку запроса # Пример: "GET / HTTP/1.1"
            first_line = rfile.readline().decode('utf-8').strip()

            if not first_line:
                return None

            # Разбиваем на метод, URL и версию протокола   # method = "GET", target = "/", version = "HTTP/1.1"
            method, target, version = first_line.split()

            # Читаем заголовки
            headers = self.parse_headers(rfile)

            # Читаем тело запроса для POST
            body = None
            if method == 'POST' and 'Content-Length' in headers:  # Зачем проверять Content-Length? Без него мы не знаем, сколько байт читать для .read(length)
                length = int(headers['Content-Length'])
                body = rfile.read(length).decode('utf-8')
            # Создаём словарь с информацией о запросе
            return {
                'method': method,
                'target': target,  # URL с параметрами, например "/add?discipline=Math&grade=5"
                'headers': headers,
                'body': body
            }
        except:
            return None

    def parse_headers(self, rfile):
        # 4. Функция для обработки headers. Необходимо прочитать все заголовки после первой строки до появления пустой строки и сохранить их в массив.
        headers = {}
        while True:
            line = rfile.readline().decode('utf-8').strip()
            if not line:  # Пустая строка - конец заголовков
                break
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key] = value
        return headers

        # GET / HTTP/1.1
        # Host: localhost:8080          ← заголовок 1
        # User-Agent: Mozilla/5.0       ← заголовок 2
        #                               ← пустая строка - конец заголовков

    def handle_request(self, req):
        # 5. Функция для обработки url в соответствии с нужным методом. В случае данной работы, нужно будет создать набор условий, который обрабатывает GET или POST запрос.
        # GET запрос должен возвращать данные. POST запрос должен записывать данные на основе переданных параметров.
        method = req['method']
        target = req['target']  # '/add?discipline=Math&grade=5'

        # Разбираем параметры из URL
        params = {}
        if '?' in target:
            # Разделяем путь и параметры запроса
            path, query = target.split('?', 1)  # path = '/add' # query = 'discipline=Math&grade=5'
            params = self.parse_params(query)  # Вспомогательная функция вернет {'discipline': 'Math', 'grade': '5'}
        else:
            path = target  # Если знака ? нет → весь target и есть путь

        # Добавляем параметры из тела POST запроса
        if method == 'POST' and req['body']:
            params.update(self.parse_params(req['body']))

        # Обработка маршрутов
        if path == '/':
            return self.show_grades()  # GET запрос - показать оценки
        elif path == '/add' and method == 'POST':
            return self.add_grade(params)  # POST запрос - добавить оценку
        else:
            return self.make_response(404, 'Not Found', '<h1>404 - Не найдено</h1>')

    def parse_params(self, query):
        """Вспомогательная функция для парсинга параметров с декодированием URL"""
        params = {}
        if query:
            for item in query.split('&'):
                if '=' in item:
                    key, value = item.split('=', 1)
                    # Декодируем URL-encoded символы
                    params[unquote(key)] = unquote(value)
        return params

    def show_grades(self):
        """Обработка GET запроса - отображение страницы с оценками"""
        # Загружаем HTML шаблон
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html = f.read()
        except:
            html = '<h1>Ошибка загрузки страницы</h1>'

        # Генерируем таблицу с оценками
        if self._grades:
            table = '<table>\n<tr><th>Дисциплина</th><th>Оценки</th></tr>\n'
            for discipline, grades in sorted(self._grades.items()):
                grades_str = ', '.join(map(str, grades))
                table += f'<tr><td>{discipline}</td><td>{grades_str}</td></tr>\n'
            table += '</table>'
        else:
            table = '<p>Нет оценок. Добавьте первую оценку!</p>'

        # Вставляем таблицу в HTML шаблон
        html = html.replace('<!--GRADES_TABLE-->', table)
        return self.make_response(200, 'OK', html)

    def add_grade(self, params):
        """Обработка POST запроса - добавление новой оценки"""
        discipline = params.get('discipline', '')
        grade_str = params.get('grade', '')

        # Проверяем, что все данные указаны
        if not discipline or not grade_str:
            return self.make_response(400, 'Bad Request', '<h1>Не указаны данные</h1>')

        # Валидация оценки
        try:
            grade = int(grade_str)
            if grade < 1 or grade > 5:
                return self.make_response(400, 'Bad Request', '<h1>Оценка должна быть от 1 до 5</h1>')
        except:
            return self.make_response(400, 'Bad Request', '<h1>Некорректная оценка</h1>')

        # Сохраняем оценку в хранилище
        if discipline not in self._grades:
            self._grades[discipline] = []  # Создание нового списка для новой дисциплины
        self._grades[discipline].append(grade)

        # Перенаправляем на главную страницу
        headers = [('Location', '/')]
        return {'status': 303, 'reason': 'See Other', 'headers': headers, 'body': ''}

    def send_response(self, conn,
                      resp):  # conn — сокетное соединение с клиентом (браузером) resp — словарь с информацией об ответе
        # 6. Функция для отправки ответа.
        # Необходимо записать в соединение status line вида HTTP/1.1 <status_code> <reason> (Создаёт строку вида: text HTTP/1.1 200 OK).
        # Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков.
        wfile = conn.makefile('wb')  # 'wb' — режим: write (запись), binary (бинарный)

        # Status line
        wfile.write(f"HTTP/1.1 {resp['status']} {resp['reason']}\r\n".encode('utf-8'))

        # Headers
        for key, value in resp.get('headers', []):
            wfile.write(f"{key}: {value}\r\n".encode('utf-8'))
        wfile.write(b'\r\n')  # Пустая строка - конец заголовков

        # Body
        if 'body' in resp and resp['body']:
            wfile.write(resp['body'].encode('utf-8'))  # Записывает байты в сокет

        wfile.flush()
        wfile.close()

    def make_response(self, status, reason, body):
        """Вспомогательная функция для создания ответа"""
        headers = [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(body.encode('utf-8'))))
        ]
        return {'status': status, 'reason': reason, 'headers': headers, 'body': body}


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    name = 'localhost'

    serv = MyHTTPServer(host, port, name)  # Создание экземпляра класса сервера
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
