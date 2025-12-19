Для запуска веб-приложения в режиме разработки выполните команду:

```
cd students/k3339/Alexey_Malakhov/lab_3/
sudo docker compose up -d                     # запуск контейнера с postgresql
cd backend
python -m venv .venv                          # создание виртуального окружения
source .venv/bin/activate                     # активация виртуального окружения
pip install -r requirements.txt               # установка зависимостей
uvicorn src.main:app --port 8000 --reload     # запуск веб-сервера
```

После успешного запуска откройте веб-интерфейс: [http://localhost:8000/](http://localhost:8000/)
