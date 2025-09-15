from typing import List
from urllib.parse import parse_qs, unquote_plus

from models import Cat

cats_list: List[Cat] = []


def generate_html_page() -> str:
    page = "<html><head><title>Каталог котиков</title>"
    page += "<meta charset='utf-8'>"
    page += "<style> body { font-family: sans-serif; } .container { max-width: 600px; margin: auto; padding: 20px; } table { width: 100%; border-collapse: collapse; } th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; } form { margin-top: 25px; padding: 15px; border: 1px solid #ccc; border-radius: 5px; } </style>"
    page += "</head><body><div class='container'>"
    page += "<h1>🐱 Каталог котиков</h1>"

    if cats_list:
        page += "<table border='1'><tr><th>Имя</th><th>Возраст (месяцев)</th></tr>"
        for cat in cats_list:
            page += f"<tr><td>{cat.name}</td><td>{cat.age_months}</td></tr>"
        page += "</table>"
    else:
        page += "<p>Вы еще не добавили ни одного котика.</p>"

    page += "<h2>Добавить нового котика</h2>"
    page += "<form method='POST'>"
    page += "Имя: <input type='text' name='name' required><br><br>"
    page += "Возраст в месяцах: <input type='number' name='age_months' required><br><br>"
    page += "<input type='submit' value='Добавить котика'>"
    page += "</form>"
    page += "</div></body></html>"
    return page


def parse_request(request: str):
    lines = request.split('\r\n')
    request_line = lines[0]
    method, path, _ = request_line.split(' ')
    body = ""
    if "" in lines:
        body_start_index = lines.index("") + 1
        body = "\n".join(lines[body_start_index:])
    return method, path, body


def main_router(request: str) -> bytes:
    method, path, body = parse_request(request)

    if method == "GET" and path == "/":
        html_content = generate_html_page()
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(html_content.encode('utf-8'))}\r\n\r\n{html_content}"
        return response.encode('utf-8')

    elif method == "POST" and path == "/":
        # parse_qs: key=val&key2=val2 -> dict
        form_data = parse_qs(unquote_plus(body))
        cat_name = form_data.get('name', [''])[0]
        age_str = form_data.get('age_months', [''])[0]

        if cat_name and age_str.isdigit():
            new_cat = Cat(name=cat_name, age_months=int(age_str))
            cats_list.append(new_cat)
            print(f"Добавлен котик: {new_cat}")

        response = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
        return response.encode('utf-8')

    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Страница не найдена</h1>"
        return response.encode('utf-8')
