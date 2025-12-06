## В данном репозитории находится API для социальной сети ITMO

### Запуск
Для начала необходимо установить необходимые переменные окружения
*   **Настройки базы данных:**
    
    *   `DB_NAME`: Имя базы данных PostgreSQL. Пример: `postgres`.
    *   `DB_USER`: Имя пользователя для подключения к базе данных PostgreSQL. Пример: `postgres`.
    *   `DB_PASSWORD`: Пароль для подключения к базе данных PostgreSQL. Пример: `test`.
*   **Настройки JWT:**
    
    *   `JWT_SECRET_KEY`: Секретный ключ для подписи токенов JSON Web Tokens (JWT). Пример: `test`.
*   **Настройки S3 (MinIO):**
    
    *   `S3_ACCESS_KEY`: Ключ доступа (используется и для MinIO). Пример: `minio`.
    *   `S3_SECRET_KEY`: Секретный ключ. Пример: `minio123`.
    *   `S3_BUCKET`: Имя бакета Amazon S3. Пример: `images`.
    *   `S3_URL`: URL для доступа к S3. Для локального MinIO в docker-compose: `http://minio:9000`.

#### Быстрый запуск с готовыми переменными
В каталоге `laboratory_work_3/lab` есть скрипт `run_with_env.sh` с дефолтными значениями. Запустит Postgres, MinIO и API:

```bash
./run_with_env.sh
```
