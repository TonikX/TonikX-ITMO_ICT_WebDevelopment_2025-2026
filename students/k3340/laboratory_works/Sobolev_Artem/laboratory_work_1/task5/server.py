import json
import socket
import sys
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse

MAX_LINE = 64*1024
MAX_HEADERS = 100

class MyHTTPServer:
  def __init__(self, host, port, server_name):
    self._host = host
    self._port = port
    self._server_name = server_name
    self._grades = {}


  def serve_forever(self):
    # Запуск сервера на сокете, обработка входящих соединений
    serv_sock = socket.socket(
      socket.AF_INET,
      socket.SOCK_STREAM,
      proto=0)

    try:
      serv_sock.bind((self._host, self._port))
      serv_sock.listen()

      while True:
        conn, _ = serv_sock.accept()
        try:
          self.serve_client(conn)
        except Exception as e:
          print('Client serving failed', e)
    finally:
      serv_sock.close()

  def serve_client(self, conn):
    # Обработка клиентского подключения
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
      #  функция для обработки заголовка http+запроса
      rfile = conn.makefile('rb')
      method, target, ver = self.parse_request_line(rfile)
      headers = self.parse_headers(rfile)
      host = headers.get('Host')
      if not host:
          raise HTTPError(400, 'Bad request', 'Host header is missing')
      return Request(method, target, ver, headers, rfile)

  def parse_request_line(self, rfile):
    raw = rfile.readline(MAX_LINE + 1)
    if len(raw) > MAX_LINE:
      raise HTTPError(400, 'Bad request',
        'Request line is too long')

    req_line = str(raw, 'iso-8859-1')
    words = req_line.split()
    if len(words) != 3:
      raise HTTPError(400, 'Bad request',
        'Malformed request line')

    method, target, ver = words
    if ver != 'HTTP/1.1':
      raise HTTPError(505, 'HTTP Version Not Supported')
    return method, target, ver

  def parse_headers(self, rfile):
    # Функция для обработки headers
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

  def handle_request(self, req):
    # Функция для обработки url в соответствии с нужным методом.
    if req.path == '/grade' and req.method == 'POST':
      return self.handle_post_grade(req)

    if req.path in ('/', '/grades') and req.method == 'GET':
      return self.handle_get_grades(req)

    raise HTTPError(404, 'Not found')

  def send_response(self, conn, resp):
    #  Функция для отправки ответа
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
    resp = Response(status, reason,
                   [('Content-Length', len(body))],
                   body)
    self.send_response(conn, resp)

  def handle_post_grade(self, req):
      discipline = (req.query.get('discipline') or [None])[0]
      grade = (req.query.get('grade') or [None])[0]

      # Если параметр не получен из строки запроса, то проверяются параметры в теле запроса
      if not discipline or not grade:
          ctype = (req.headers.get('Content-Type') or '').split(';', 1)[0].strip()
          if ctype == 'application/x-www-form-urlencoded':
              # Чтение тела запроса
              raw = req.body()
              if raw:
                  data = parse_qs(raw.decode('utf-8'), keep_blank_values=True)
                  discipline = (data.get('discipline') or [None])[0]
                  grade = (data.get('grade') or [None])[0]

      if not discipline or not grade:
          raise HTTPError(400, 'Bad request', 'Fields "discipline" and "grade" are required')

      self._grades.setdefault(discipline, []).append(str(grade))

      headers = [('Location', '/'), ('Content-Length', '0'), ('Connection', 'close')]
      return Response(303, 'See Other', headers, b'')

  def handle_get_grades(self, req):
      # Извлечение данных из заголовка
      accept = req.headers.get('Accept', '')

      # Возвращение ответа в виде json
      if 'application/json' in accept:
          # сериализация словарь в json
          body = json.dumps(self._grades, ensure_ascii=False).encode('utf-8')
          headers = [
              ('Content-Type', 'application/json; charset=utf-8'),
              ('Content-Length', str(len(body)))
          ]
          return Response(200, 'OK', headers, body)

      items = []
      if self._grades:
          for disc, grades in sorted(self._grades.items()):
              items.append(f'<li>{disc}: {", ".join(grades)}</li>')
          items_html = '\n'.join(items)
      else:
          items_html = '<li><em>Пока нет оценок</em></li>'

      with open("Lab1/task5/index.html", "r", encoding="utf-8") as f:
          template = f.read()

      html = template.format(
          items_html=items_html,
          count=len(self._grades)
      )

      body = html.encode('utf-8')
      headers = [
          ('Content-Type', 'text/html; charset=utf-8'),
          ('Content-Length', str(len(body)))
      ]
      return Response(200, 'OK', headers, body)


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

  def body(self):
      size = self.headers.get('Content-Length')
      if not size:
          return b''
      try:
          n = int(size)
      except ValueError:
          raise HTTPError(400, 'Bad Request', 'Invalid Content-Length')
      return self.rfile.read(n)

class Response:
  def __init__(self, status, reason, headers=None, body=None):
    self.status = status
    self.reason = reason
    self.headers = headers
    self.body = body

class HTTPError(Exception):
  def __init__(self, status, reason, body=None):
    super()
    self.status = status
    self.reason = reason
    self.body = body


if __name__ == '__main__':
  host = sys.argv[1]
  port = int(sys.argv[2])
  name = sys.argv[3]

  serv = MyHTTPServer(host, port, name)
  try:
    serv.serve_forever()
  except KeyboardInterrupt:
    pass