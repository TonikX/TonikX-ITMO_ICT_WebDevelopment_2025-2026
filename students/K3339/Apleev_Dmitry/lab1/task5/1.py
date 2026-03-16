import json
import socket
import os
import urllib.parse


def load_grades():
    if os.path.exists("grades.json"):
        with open("grades.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_grades(grades_list):
    with open("grades.json", 'w', encoding='utf-8') as f:
        json.dump(grades_list, f)

def dec_russian(text):
    return urllib.parse.unquote_plus(text, encoding='utf-8')

def create_page(grades_list):
    page = "<html><head><meta charset='UTF-8'><title>Оценки</title></head><body>"
    page += "<h1>Мои оценки</h1>"

    page += "<form method='POST'>"
    page += "Предмет: <input name='subject'><br>"
    page += "Оценка: <input name='grade'><br>"
    page += "<input type='submit' value='Добавить'>"
    page += "</form>"

    page += "<h2>Список оценок:</h2>"
    page += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse; width: 100%;'>"
    page += "<tr><th>№</th><th>Предмет</th><th>Оценки</th></tr>"

    if not grades_list:
        page += "<tr><td colspan='3'>Пока нет оценок</td></tr>"
    else:
        for i, item in enumerate(grades_list):
            subject = item.get('subject')
            grades = item.get('grades')
            grades_text = ', '.join(str(g) for g in item['grades'])
            page += f"<tr><td>{i + 1}</td><td>{subject}</td><td>{grades_text}</td></tr>"
    page += "</table></body></html>"
    return page


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9099))
    server.listen()

    print(f"Сервер запущен на http://localhost:9099")

    while True:
        client, addr = server.accept()
        request = client.recv(1024).decode('utf-8')

        if not request:
            client.close()
            continue
        # GET или POST
        lines = request.split('\n')
        first_line = lines[0]

        if 'GET' in first_line:
            method = 'GET'
        elif 'POST' in first_line:
            method = 'POST'
        else:
            break

        grades = load_grades()

        if method == 'GET':
            html_page = create_page(grades)
            response = "HTTP/1.1 200 OK\n"
            response += "Content-Type: text/html; charset=utf-8\n\n"
            response += html_page

        elif method == 'POST':
            form_data = ""
            for i, line in enumerate(lines):
                if line.strip() == '' and i + 1 < len(lines):
                    form_data = lines[i + 1]
                    break

            subject = ""
            grade = ""

            if 'subject=' in form_data:
                subject_part = form_data.split('subject=')[1]
                if '&' in subject_part:
                    subject = subject_part.split('&')[0]
                else:
                    subject = subject_part

            if 'grade=' in form_data:
                grade_part = form_data.split('grade=')[1]
                grade = grade_part

            if subject:
                subject = dec_russian(subject)
            if grade:
                grade = dec_russian(grade)

            if subject and grade:
                found = False
                for item in grades:
                    if item.get('subject') == subject:
                        if 'grades' not in item:
                            item['grades'] = []
                        item['grades'].append(grade)
                        found = True
                        break

                if not found:
                    new_item = {'subject': subject, 'grades': [grade]}
                    grades.append(new_item)

                save_grades(grades)

            html_page = create_page(grades)
            response = "HTTP/1.1 200 OK\n"
            response += "Content-Type: text/html; charset=utf-8\n\n"
            response += html_page

        client.send(response.encode('utf-8'))
        client.close()

if __name__ == "__main__":
    main()