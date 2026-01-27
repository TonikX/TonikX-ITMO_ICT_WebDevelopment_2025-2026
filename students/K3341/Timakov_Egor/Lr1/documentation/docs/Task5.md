## Выполнение пятого пункта лабораторной работы

В данном задании нам, нужно записать информацию о дисциплинах и оценках по дисциплине, и выдавать результат виде html-странички

Для начала запускаем многопоточный TCP-сервер 
```
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
```

Далее мы принимаем соединение, и отдаем запрос в отдельный поток

Функция, которая обрабатывает запрос клиента для начала проверяет не пустой ли запрос.
Затем мы Парсим первую строчку запроса для определения метода и пути
В случае если это get запрос то мы просто отправляем html-страницу
``` 
        if method == 'GET':
            if path == '/':
                html_body = get_html_page()
                response = build_response(200, "text/html", html_body)
            else:
                response = build_response(404, "text/html", "<h1>404 Not Found</h1>")

            conn.sendall(response)
```

В случае если это post запрос, то сервер парсит данные из тела запроса и обновляет словарь, и после редиректим пользователя.
``` 
        elif method == 'POST':
            
            if path == '/':
                # Находим тело POST-запроса (после пустой строки)
                body_start = request_data.find('\r\n\r\n') + 4
                post_body = request_data[body_start:].strip()

                params = parse_qs(post_body)

                discipline = params.get('discipline', [''])[0].strip()
                grade = params.get('grade', [''])[0].strip()

                if discipline and grade:
                    with data_lock:
                        grades_data[discipline] = grade
                    print(f"Сохранена новая оценка: {discipline} -> {grade}")

                    
                    response = build_response(303, "text/html", "")
                else:
                    response = build_response(200, "text/html", "<h1>Ошибка: Неполные данные</h1>")

                conn.sendall(response)

            else:
                response = build_response(404, "text/html", "<h1>404 Not Found</h1>")
                conn.sendall(response)
```

Также на сервере есть функция которая занимается генерированием html страницы. 
