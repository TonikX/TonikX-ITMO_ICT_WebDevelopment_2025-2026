import socket
from typing import Dict, Optional, List
from urllib.parse import parse_qs


class Request:
    '''
    Класс для хранения данных HTTP-запросов

    Атрибуты:
        method (str): HTTP-метод запроса ('GET', 'POST', ...)
        addr (str): путь или ресурс из URL без параметров запроса
        param (str): параметры запроса в URL после знака '?'
        version_proto (str): версия протокола HTTP запроса
        headers (Optional[Dict[str, str]]): словарь HTTP-заголовков, где ключ — имя заголовка, а значение — соответствующее ему значение
        body (str): тело HTTP-запроса (текстовое содержимое)
    '''
    def __init__(self,
                 method: str,
                 addr: str,
                 param: str,
                 version_proto: str,
                 headers: Optional[Dict[str, str]] = None,
                 body: str = '') -> None:
        self.method = method
        self.addr = addr
        self.param = param
        self.version_proto = version_proto
        self.headers = headers or {}
        self.body = body


class MyHTTPServer:
    '''
    Класс HTTP-сервера на основе сокетов
    '''
    def __init__(self, host: str, port: int, server_name: Optional[str] = None) -> None:
        self._host = host
        self._port = port
        self._server_name = server_name

        # хранит оценки по дисциплинам
        self.grades: Dict[str, List[int]] = {}  # {дисциплина: список оценок}


    def serve_forever(self) -> None:
        '''
        Запуск сервера на сокете, слушает и обрабатывает входящие соединения
        '''
        # Запускаем новый сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self._host, self._port))
            server.listen(1) # Работает одновременно только с одним подключением
            print(f'Сервер слушает на {self._host}:{self._port}')

            # Запускаем бесконечное прослушивание подключённого клиента
            while True:
                conn, _ = server.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print(f'Ошибка клиента: {e}')
                finally:
                    conn.close()  # закрываем соединение после обработки запроса


    def serve_client(self, conn: socket.socket) -> None:
        '''
        Обрабатывает запрос клиента, используя методы парсинга запроса и заголовков
        '''
        # файловый объект для удобного чтения в потоке
        stream = conn.makefile('rb')
        # парсим запросы и заголовки
        request = self.parse_request(stream)  # --> Request
        headers = self.parse_headers(stream)

        # тк request возвращается из метода parse_request как экземпляр класса Request, то нам доступны все его переменные
        request.headers = headers

        content_length = int(headers.get('Content-Length', '0'))
        if content_length > 0:
            # Если тело HTTP запроса есть (POST), читаем ровно content_length байт из потока
            request.body = stream.read(content_length).decode('utf-8')
        else:
            request.body = ''

        # Передаём распарсенный запрос в хэндлер бизнес-логики, он уже решит, что с запросом делать
        self.handle_request(conn, request)

    def parse_request(self, stream) -> Request:
        '''
        Парсит первую строку HTTP-запроса (request line) и возвращает
        объект Request с методом, адресом, параметрами и версией протокола
        '''
        request_line = stream.readline().decode('utf-8').strip()

        if not request_line:
            raise ValueError('Отсутствует request line')

        method, url, version_proto = request_line.split(' ')
        addr, *param = url.split('?', 1)
        # если параметры не были переданы
        param = param[0] if param else ''

        return Request(method, addr, param, version_proto)


    def parse_headers(self, stream) -> Dict[str, str]:
        '''
        Парсит HTTP-заголовки из потока до пустой строки
        '''
        # next(request_lines)  # пропускаем request line, работаем долько с заголовками

        headers = {}

        while True:
            line = stream.readline().decode('utf-8').strip()
            # останавливаем поток когда доходим до пустой строки
            if not line:
                break
            if ': ' in line:
                header, value = line.split(': ')
                headers[header] = value

        return headers


    def handle_request(self, conn: socket.socket, req: Request) -> None:
        '''
        Логика обработки HTTP-запросов (GET, POST)
        '''

        # GET /grades -- получить список всех оценок
        if req.method == 'GET' and req.addr == '/grades':
            # формируем HTML страничку и отправляем с 200 кодом
            response_html = self._render_grades_page()
            self.send_response(conn, 200, 'OK', response_html)

        # POST /grades?subject=*&grade=* -- записать новую оценку по дисциплине
        # в теле запроса только (x-www-form-urlencoded)
        if req.method == 'POST' and req.addr == '/grades':
            # Принимаем данные из тела и обновляем оценки
            form = parse_qs(req.body)
            subject = form.get('subject', [''])[0]
            grade = form.get('grade', [''])[0]

            # Если есть и предмет, и оценка
            if subject and grade:
                if subject not in self.grades:
                    self.grades[subject] = []
                # Сохраняем предмет и оценку
                self.grades[subject].append(int(grade))
                # Возвращаем HTML-страницу со всеми оценками + новая оценка
                response_html = self._render_grades_page()
                self.send_response(conn, 200, 'OK', response_html)
            else:
                # При ошибке получения дисциплины или оценки кидаем 400 ошибку
                self.send_response(conn, 400, 'Bad Request', '<h2>Ошибка: в body не заданы subject или grade</h2>')


    def send_response(self,
                      conn: socket.socket,
                      code: int,
                      reason: str,
                      body: str,
                      content_type: str = 'text/html; charset=utf-8') -> None:
        '''
        Функция формирует и отправляет HTTP-ответ
        '''
        response_headers = [
            f'HTTP/1.1 {code} {reason}',
            f'Content-Type: {content_type}',
            f'Content-Length: {len(body.encode("utf-8"))}',
            '',
            '',
        ]

        # Переводим заголовки и тело в байты
        header_bytes = '\r\n'.join(response_headers).encode('utf-8')
        body_bytes = body.encode('utf-8')

        # Отправка заголовков и тела
        conn.sendall(header_bytes + body_bytes)


    def _render_grades_page(self) -> str:
        '''
        Рендерит (формирует) HTML-страницу со всеми оценками
        '''
        # Формируем строки в таблице (дисциплина -- оценка)
        rows = ''.join(f'<tr><td>{discipline}</td><td>{", ".join(map(str, grade))}</td></tr>' for discipline, grade in self.grades.items())

        # структура HTML-страницы
        html = f"""
        <html>
            <head>
                <title>Оценки по дисциплинам</title>
            </head>
            <body>
                <h1>Оценки студентов</h1>
                <table border="1" cellpadding="5" cellspacing="0">
                    <tr>
                        <th>Дисциплина</th>
                        <th>Оценки</th>
                    </tr>
                    {rows}
                </table>
            </body>
        </html>
        """

        return html


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    name = 'Grader'
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print('Сервер остановлен')
