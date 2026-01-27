## Выполнение третьего пункта лабораторной работы

В данной работе нам надо написать простой http сервер, который будет отправлять html файл клиенту через браузер

При отправлении html файла в браузер мы будем использовать TCP соединение, так как нужно соединение, которое точно дойдет до клиента.

Для начала нам нужно загрузить содержимое html-файла, затем Мы формируем полный HTTP-ответ:
```
 http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        "Connection: close\r\n"  
        "\r\n"  
        f"{html_content}"
    )
```
После этого мы создаем и настраиваем сокет:
``` 
 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        server_socket.bind((HOST, PORT))

        server_socket.listen(1)
```

Эта строчка ``server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`` Позволяет повторно использовать адресс сразу после закрытия.

Затем мы ожидаем http-запрос от клиента/браузера и отправляем http-ответ:
```
                conn, addr = server_socket.accept()
                with conn:
                    print(f"\nПолучено соединение от {addr}")

                    request = conn.recv(1024).decode('utf-8')
                    if not request:
                        continue
                    
                    conn.sendall(http_response.encode('utf-8'))
                    print(f"Ответ (файл {HTML_FILE}) отправлен.")

```



