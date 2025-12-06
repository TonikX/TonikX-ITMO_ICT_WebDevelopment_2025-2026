## В данном репозитории находится API для социальной сети ITMO

### Запуск
Для начала необходимо установить необходимые переменные окружения
*   **Настройки базы данных:**
    
    *   `DB_NAME`: Имя базы данных PostgreSQL. Пример: `postgres`.
    *   `DB_USER`: Имя пользователя для подключения к базе данных PostgreSQL. Пример: `postgres`.
    *   `DB_PASSWORD`: Пароль для подключения к базе данных PostgreSQL. Пример: `test`.
*   **Настройки JWT:**
    
    *   `JWT_SECRET_KEY`: Секретный ключ для подписи токенов JSON Web Tokens (JWT). Пример: `test`.
*   **Настройки Amazon S3:**
    
    *   `S3_ACCESS_KEY`: Ключ доступа к бакету Amazon S3. Пример: `LrK9q7NRMfwxpiQ7guln`.
    *   `S3_SECRET_KEY`: Секретный ключ для бакета Amazon S3. Пример: `v3rWd5fZ1XiKERZdgJq1VJmxhsMyoss7iBKkh21O`.
    *   `S3_BUCKET`: Имя бакета Amazon S3. Пример: `images`.
    *   `S3_URL`: URL для доступа к бакету Amazon S3. Пример: `http://12.34.56.78:9000`.

С помощью docker-compose запустите API

```bash
docker-compose up -p socnetitmo -d
```
